from django.http import JsonResponse
from .models import *
from accuont.models import User
from .serializers import AccStatusMainSerializer
import pandas as pd
def getAccreditationData(request):
    account = User.objects.filter(is_superuser=0)
    accred = [AccStatusMainSerializer(val.accstatusmain_set.all()[len(val.accstatusmain_set.all())-1]).data for val in account]    
    df = pd.DataFrame(accred)
    return JsonResponse(df['Accreditation_Status'].value_counts().to_dict())