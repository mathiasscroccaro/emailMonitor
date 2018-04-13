import datetime
import gmailreader
import gmailsender
import pygame
import pygame.camera
import os, fnmatch

class emailLib():

    def __init__(self,user,password):

        pygame.init()
        pygame.camera.init()
        self.cam = pygame.camera.Camera('/dev/video0',(640,480))

        self.user = user
        self.password = password

        self.reader = gmailreader.Gmail()
        self.reader.login(self.user,self.password)

        self.sender = gmailsender.GMail(self.user,self.password)

        self.verifyEmail()

    def verifyEmail(self):

        requests = self.reader.inbox().mail(unread=True,sender=self.user,on=datetime.date.today())

        if len(requests) is not 0:
            for request in requests:
                request.fetch()
                if  request.subject == "[GROW]":
                    #request.delete()
                    self.processQuery(request.body)

    def processQuery(self,body):

        try:
            exec(body)
            self.replyMessage()
        except:
            error = "Error at the command the command: \n\n%s" % (body)
            self.replyMessage(error)

    def generateAttachments(self):

        attachments = []

        try:
            self.cam.start()
            image = self.cam.get_image()
            self.cam.stop()

            lastImage = datetime.datetime.now().strftime("./attachments/%H-%M-%S_%d-%b-%Y.jpg")
            pygame.image.save(image,lastImage)

            attachments.append(lastImage)
        except:
            pass

        ### FIX IT - ADD TEXT WITH SENSOR DATA
        #attachments = self.find("*.txt","./attachments/")

        return attachments

    def find(self,pattern,path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name,pattern):
                    result.append(os.path.join(root,name))
        return result

    def replyMessage(self,error=""):

        subject = "[GROW - NOREPLY]"

        attach = self.generateAttachments()

        body = """
        Hello grower!

        This is a robot made reply message. Attachments are image of the grow and sensoring data.

        Program report:

        %s
        Peace out!
        """ % (error)

        msg = gmailsender.Message(subject,to=self.user,text=body,attachments=attach)
        self.sender.send(msg)
