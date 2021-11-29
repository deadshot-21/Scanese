from typing import Union
from cis.vessels import finalp
from CIS_Site.settings import BASE_DIR
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from weasyprint import HTML, CSS
import os
import glob
from django.core.files.storage import FileSystemStorage
import csv
from xhtml2pdf import pisa
import pyppdf
import time

# import matplotlib.pyplot as plt
# import numpy as np
# Create your views here.
def home(request):
     return render(request,'home.html')

def upload(request):
     files = glob.glob(os.path.join(BASE_DIR,'media/*'))
     for f in files:
          os.remove(f)
     vessel_overlayed = glob.glob(os.path.join(BASE_DIR,'static/Vessel_overlayed/*'))
     for f in vessel_overlayed:
          os.remove(f)
     vessel = glob.glob(os.path.join(BASE_DIR,'static/Vessels/*'))
     for f in vessel:
          os.remove(f)
     contour = glob.glob(os.path.join(BASE_DIR,'static/Contours/*'))
     for f in contour:
          os.remove(f)
     if request.method == 'POST' and request.FILES.getlist('myfile'):
        myfile = request.FILES.getlist('myfile')
        fs = FileSystemStorage()
        i=1
        for f in myfile:
          fs.save('slice'+str(i)+'.nii.gz', f)
          i+=1
        finalp()
        m=[]
        a=[]
        f=[]
        mean(m,a)
        labels(f,a)
        contour = glob.glob(os.path.join(BASE_DIR,'static/Contours/*'))
        vessel_overlayed = glob.glob(os.path.join(BASE_DIR,'static/Vessel_overlayed/*'))
     #    temp1 = [4,96]
        print(m,a)
        return render(request,'result.html',{'mean':m,'contour':contour,'vessel_overlayed':vessel_overlayed,'percentage':a,'frames':f})
     return render(request, 'home.html')

def result(request):
     contour=[]
     contours=[]
     vessel_overlayeds=[]
     vessel_overlayed=[]
     contours = glob.glob(os.path.join(BASE_DIR,'static/Contours/*'))
     for x in contours:
          # print(x)
          y=x.split("\\")[6]
          # print(y)
          contour.append(y)
     # contour = glob.glob(os.path.join(BASE_DIR,'static/Contours/*'))
     vessel_overlayeds = glob.glob(os.path.join(BASE_DIR,'static/Vessel_overlayed/*'))
     for x in vessel_overlayeds:
          # print(x)
          y=x.split("\\")[6]
          # print(y)
          vessel_overlayed.append(y)
     m=[]
     a=[]
     f=[]
     mean(m,a)
     # labels(f,a)
     base = 'Frame '
     for i in range(1,len(a)+1):
          temp = base + str(i)
          f.append(temp)
     print(f)
     # temp1 = [[5,95]]
     return render(request,'result.html',{'mean':m,'contour':contour,'vessel_overlayed':vessel_overlayed,'percentage':a,'frames':f})


def mean(m,a):
     #######CHANGE NAME ########
     # filename = "vessel_volumes.csv"
     filenames = glob.glob(os.path.join(BASE_DIR,'static\\csv\\*'))
     # mean=[]

# initializing the titles and rows list
     for file in filenames:
          rows = []
          with open(file, 'r') as csvfile:
               csvreader = csv.reader(csvfile)
               for row in csvreader:
                    rows.append(row)

          sum = 0
          count = 0
          temp=[]
          for row in rows:
               if len(row) != 0:
                    sum = sum + float(row[-1])
                    a.append(round(float(row[-1]),3))
                    count+=1
          mean = sum/count
          temp.append(round(mean,2))
          temp.append(round(100-mean,2))
          m.append(temp)

def labels(f,a):
     base = 'Frame '
     for i in range(len(a)):
          temp = base + str(i)
          f.append(temp)

def printPDF(request):
     contour=[]
     contours=[]
     vessel_overlayeds=[]
     vessel_overlayed=[]
     contours = glob.glob(os.path.join(BASE_DIR,'static/Contours/*'))
     for x in contours:
          # print(x)
          y=x.split("\\")[6]
          # print(y)
          contour.append(y)
     # contour = glob.glob(os.path.join(BASE_DIR,'static/Contours/*'))
     vessel_overlayeds = glob.glob(os.path.join(BASE_DIR,'static/Vessel_overlayed/*'))
     for x in vessel_overlayeds:
          # print(x)
          y=x.split("\\")[6]
          # print(y)
          vessel_overlayed.append(y)
     m=[]
     a=[]
     f=[]
     mean(m,a)
     # labels(f,a)
     base = 'Frame '
     for i in range(1,len(a)+1):
          temp = base + str(i)
          f.append(temp)
     print(f)
     # temp1 = [[5,95]]
     html_template = get_template('result.html').render({'mean':m,'contour':contour,'vessel_overlayed':vessel_overlayed,'percentage':a,'frames':f})
     # pdf_file = HTML(string=html_template).write_pdf()
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report.pdf"'
     time.sleep(10)
     pisa_status = pisa.CreatePDF(html_template, dest=response)
     if pisa_status.err:
          return HttpResponse("error")
     
     # save(args={},html=html_template,output_file=response)
     return response
     

def save(args: dict, url: str=None, html: str=None, output_file: str=None, goto: str=None, dir_: str=None) -> bytes:
     return None