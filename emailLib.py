import datetime
import gmailreader
import gmailsender

class emailLib():

    def __init__(self,user,password):

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

        pass

    def replyMessage(self):

        self.generateAttachments()

        msg = gmailsender.Message('[GROW - NOREPLY]',to='mathias.scroccaro@gmail.com',text='Hello',attachments=['img.jpg'])
        self.sender.send(msg)



        #request.fetch()
