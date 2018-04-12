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
                    request.delete()
                    self.processQuery(request.body)

    def processQuery(self,body):

        exec(body)
        self.replyMessage()

    def generateAttachments(self):

        self.cam.start()
        image = self.cam.get_image()
        self.cam.stop()

        lastImage = datetime.datetime.now().strftime("attachments/%H:%M:%S-%d-%m-%y.jpg")
        pygame.image.save(image,lastImage)

        ### FIX IT - ADD TEXT WITH SENSOR DATA
        #attachments = self.find("*.txt","./attachments/")
        attachments = []

        return attachments.append(lastImage)

    def find(self,pattern,path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name,pattern):
                    result.append(os.path.join(root,name))
        return result

    def replyMessage(self):

        subject = "[GROW - NOREPLY]"

        body = """
        Hello grower!

        This is a robot made reply message. Attachments are image of the grow and sensoring data.

        Peace out!
        """

        msg = gmailsender.Message(subject,to=self.user,text=body,attachments=self.generateAttachments())
        self.sender.send(msg)
