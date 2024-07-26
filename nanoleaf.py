import requests
import json
import os
import time
import random
import pickle as p
import string

key=os.environ.get('API_KEY')


position_prompt = '''Generate a list of lightbulb IDs and RGB codes from an array of usable IDs 
and a text prompt. The data you return should correspond to the text prompt 
you are given along with the ID data you are given. Please return your data in this format: 
"<ID>,r,g,b,<ID>,r,g,b..." for example with prompt "WHITE" and ID list [[1, {x:12, y:20}], [2, {x:32, y:0}], [3, {x:120, y:300}]] you will return 
"1, 255, 255, 255, 2, 255, 255, 255, 3, 255, 255, 255"
However, make sure to also analyse the x and y positions of the lights to display what the user wants. For example, if the prompt was "Red at the bottom, blue at the top", you should use reasoning to then generate the data in a relevent way using the x and y positions that you were given.
If you know certain IDs are at the top, if the user is asking for something specific at the top, you should set those to what the user wants, and vice versa for every position.
Do not include anything else in your response, besides the list of IDs and color codes in the format you were given. Make sure to not include any quote marks: " and make sure never to set an ID to black (0, 0, 0)'
'''


original = '''Generate a list of IDs and RGB codes from an array of usable IDs 
and a text prompt. The data you return should correspond to the text prompt 
you are given along with the ID data you are given. Please return your data in this format: 
"<ID>,r,g,b,<ID>,r,g,b..." for example with prompt "WHITE" and ID list [1, 2, 3] you will return 
"1, 255, 255, 255, 2, 255, 255, 255, 3, 255, 255, 255"
 Do not include anything else in your response, besides the list of IDs and color codes in the format you were given'''

class NanoleafConnection():
    def __init__(self, addr, token):
        self.http = 'http://'+addr+':16021'
        self.token = token
        self.lCommand = []


    def isOn(self, on):
        req = requests.put(self.http + '/api/v1/' + self.token + '/state', data=json.dumps({'on':{'value':on}}))
        # if req.status_code == 204:
        #     print('Successful with return: ' + req.text)


    def setBrightness(self, percent, duration):
        req = requests.put(self.http + '/api/v1/' + self.token + '/state', data=json.dumps({'brightness':{'value':percent, 'duration':duration}}))
        # if req.status_code == 204:
        #     print('Successful with return: ' + req.text)


    def setColor(self, hue, saturation, temperature):
        req = requests.put(self.http + '/api/v1/' + self.token + '/state', data=json.dumps({'hue':{'value':hue}, 'sat':{'value':saturation}, 'ct': {'value':temperature}}))
        # if req.status_code == 204:
        #     print('Successful with return: ' + req.text)


    def getLayout(self, verbose=False, position=True):
        get = requests.get(self.http+'/api/v1/'+self.token+'/panelLayout/layout')
        if verbose:
            print('____ID_____POSITION___')
        retList = []
        for x in json.loads(get.text)['positionData']:
            if verbose:
                print(' ' + str(x['panelId']) + '    ' + str(x['x']) + ', ' + str(x['y']))
            if position:
                retList.append([x['panelId'], {'x':x['x'],'y':x['y']}])
            else:
                retList.append(x['panelId'])
        return retList
            
    

    def addCommand(self, id, rgb):
        self.lCommand.append([id, rgb])


    def sendEffect(self, seconds=False):
        anim = str(len(self.lCommand))
        if seconds:
            seconds*=10
        else:
            seconds=0
        for x in self.lCommand:
            anim+=(' ' + str(x[0]) + ' 1 ' + str(x[1][0]) + ' ' + str(x[1][1]) + ' ' + str(x[1][2]) + ' 0 ' + str(seconds))
        #print(anim)
        send = {
        "command": "display",
        "animType": "static",
        "animData": anim,
        "loop": False,
        "palette": [{
            "hue": 0,
            "saturation": 100,
            "brightness": 0
        }, {
            "hue": 30,
            "saturation": 100,
            "brightness": 10
        }],
        "colorType": "HSB"
        }
        req = requests.put(self.http + '/api/v1/' + self.token + '/effects', data=json.dumps({'write':send}))
        return req.status_code
    
def loadPreset(nl, filename=None):
    if filename == None:
        pickleFiles = []
        for file in os.listdir("./"):
            if file.endswith(".p"):
                pickleFiles.append(file)
        print('Which pickle file would you like to load? \n__________________________________________')
        i=0
        for file in pickleFiles:
            print('[' + str(i) + '] - ' + file)
            i+=1
        try:
            selection = int(input('>> '))
        except:
            proceed=False
            while proceed==False:
                print('[X] Selection must be a valid number [X]')
                selection = input('>> ')
                try:
                    selection=int(selection)
                    proceed=((selection<=(len(pickleFiles)-1) and (selection>=0)))
                except:
                    proceed=False
            
            
        filename=pickleFiles[selection]
        
    with open(filename, 'rb') as f:

        saved_data = p.load(f) # deserialize using load()
        interator = 0
        parse = []
        for x in saved_data.split(','):
            if interator<4:
                parse.append(int(x))
                interator+=1
                #print('Iterator Debug: ', interator)
            else:
                #print('Parse Debug ', parse)
                nl.addCommand(parse[0], [parse[1], parse[2], parse[3]])
                interator=0
                parse=[]
                parse.append(int(x))
                interator+=1
                #print('Iterator Debug: ', interator)
            
        nl.sendEffect(seconds=False)

def savePreset(prompt, returnData):
    filename = prompt.split(' ')[0] + '-' + prompt.split(' ')[1] + '_' + ''.join(random.choice(string.ascii_letters) for i in range(4)) + '.p'
    print('Saving to ' + filename)
    with open(filename, 'wb') as f:
        p.dump(returnData, file=f, protocol=None, fix_imports=True, buffer_callback=None)
    f.close()

def generateColors(prompt, model, api_key, nl, understands_position=True):
    genPrompt=position_prompt
    layoutData = nl.getLayout(position=understands_position)
    if understands_position != True:
        genPrompt=original
    
    data = {"model":model,"messages":[{"role":"system", "content":genPrompt}, {"role":"user", "content":"ID List: " + str(layoutData) + ", Prompt: " + prompt}]}
    print("Posting to /chat/completions...")
    gpt4o = requests.post('https://api.openai.com/v1/chat/completions', data=json.dumps(data), headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    response = json.loads(gpt4o.text)
    returnData = response['choices'][0]['message']['content']
    print('Done.')
    print('Return Data', returnData)
    interator = 0
    parse = []
    for x in returnData.split(','):
        if interator<4:
            parse.append(int(x))
            interator+=1
            #print('Iterator Debug: ', interator)
        else:
            #print('Parse Debug ', parse)
            nl.addCommand(parse[0], [parse[1], parse[2], parse[3]])
            interator=0
            parse=[]
            parse.append(int(x))
            interator+=1
            #print('Iterator Debug: ', interator)
        
    nl.sendEffect(seconds=False)
    save = input("Would you like to save this preset? (Y/N) \n>> ")
    if save == "Y":
        savePreset(prompt, returnData)

        




    
def demo():
    nl = NanoleafConnection(os.environ.get("NANOLEAF_IP"), os.environ.get("NANOLEAF_KEY"))
    nl.isOn(False)
    layout = nl.getLayout()
    print('__________________________\n\n     Nanoleaf AI Demo     \n__________________________')
    time.sleep(0.35)
    print('• Create preset - [0]')
    time.sleep(0.35)
    print('• Load a preset - [1]')
    time.sleep(0.35)
    try:
        choice = int(input('[0-1] >> '))
        if not(choice==0 or choice==1):
            raise(Exception)
    except:
        
        proceed=False
        while proceed==False:
            print('[X] Selection must be a valid number from 0-1 [X]')
            choice = input('>> ')
            try:
                choice=int(choice)
                proceed=(((choice==0) or (choice==1)))
                print(proceed)
            except:
                proceed=False
    if choice == 0:
        uPosInput = input('Use V1 controller or V2 (V2 understands position)\n>> ')
        uPos = True
        if uPosInput.lower()=='v1':
            uPos==False
        generateColors(input("gpt-4o text prompt >> "), 'gpt-4o', key, nl, understands_position=uPos)
    elif choice == 1:
        loadPreset(nl)

if __name__ == "__main__":
    demo()