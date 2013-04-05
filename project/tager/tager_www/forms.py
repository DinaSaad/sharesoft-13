from django import forms
from tager_www.models import *

class BuyerIdentificationForm(forms.Form):
    buyer_phone_num = forms.CharField(max_length=12)
    
    def GetBuyerNum(self):
        
        #buyer_number = self.cleaned_data["buyer_phone_num"]
        return self.buyer_phone_num
    
    
        
