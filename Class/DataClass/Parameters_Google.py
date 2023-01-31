class Parameters_G:
    def __init__(self, _Keywords, _Nb_Results, _Language, _Domain) -> None:
        self.Keywords = _Keywords 
        self.Nb_Results = _Nb_Results 
        self.Language = _Language
        self.Domain = _Domain
        self.Url = "https://www.google.com/search?q="

        self.set_URL()

    def set_URL(self) -> None:
        list_keywords = self.Keywords.split()

        for i in range(len(list_keywords)):
            if i != len(list_keywords)-1:
                self.Url+= list_keywords[i] + "+"
            else:
                self.Url+= list_keywords[i] 

        self.Url += "&num=" + str(self.Nb_Results)


