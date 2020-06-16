from django.dispatch import Signal, receiver


inform = Signal(providing_args=['data']) # Signal informer
class Word(models.Model):
    name = models.CharField(max_length=50)
    date_updated = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    lemma = models.ForeignKey('Lemma', on_delete=models.PROTECT, null=True)
    language = models.ForeignKey(
        'Language',
        on_delete=models.PROTECT,
        null=True
    )
    tagset = models.ForeignKey('TagSet', on_delete=models.PROTECT, null=True)

    """ 
        Overriding the save method to send the signal
        for appending new words to the download files
    """
    def save(self, *args, **kwargs):
        super(Word, self).save(*args, **kwargs)
        inform.send(sender=self, data=[self.name, self.lemma, self.tagset, self.language])

    def __str__(self):
        return self.name



@receiver(inform)
def appendToFile(sender, **kwargs):
    """ Receives signal from the save() method in the Word model 
        When a new word is created, then append this data in the .csv file.
    """
    Object = (kwargs.get('data'))
    
    wordName = Object[0]
    lemmaName= Object[1].name
    tagsetName = Object[2].name
    languageName = Object[3].name


    filename = "".join(["data/langs/Complete/", languageName, ".csv"])
    # print(filename)
    lineToAppend = " ".join([lemmaName, wordName, tagsetName,'\n'])
    # print(lineToAppend)

    # with open(filename,'a') as file:
    #     file.write(lineToAppend)
