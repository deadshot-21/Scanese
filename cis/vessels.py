import csv
import glob
from CIS_Site.settings import BASE_DIR
from cis.utils import *

# basepath = './Images/slice*.nii.gz'
# vessels = './Vessels/'
# figures = './Figures/'
# overlay_path = './Vessel_overlayed/'
# paths = sorted(glob.glob(basepath))
# myFile = open('vessel_volumes.csv', 'w')
# lung_areas_csv = []
# ratios = []

# make_dirs(vessels)
# make_dirs(overlay_path)
# make_dirs(figures)


def finalp():
# D:\Projects\Image Processing Site\Site\CIS_Site\static\Vessels
     basepath = os.path.join(BASE_DIR,'media\\slice*.nii.gz')
     vessels = os.path.join(BASE_DIR,'static\\Vessels\\')
     # figures = os.path.join(BASE_DIR,'static\\Figures\\')
     # outpath = os.path.join(BASE_DIR,'static\\Lungs\\')
     contour_path = os.path.join(BASE_DIR,'static\\Contours\\')
     # contour_path = './Contours/'
     overlay_path = os.path.join(BASE_DIR,'static\\Vessel_overlayed\\')
     paths = sorted(glob.glob(basepath))
     csv_path = os.path.join(BASE_DIR,'static\\csv\\')
     
     lung_areas_csv = []
     ratios = []

     def create_vessel_mask(lung_mask, ct_numpy, denoise=False):
          vessels = lung_mask * ct_numpy  # isolate lung area
          vessels[vessels == 0] = -1000
          vessels[vessels >= -500] = 1
          vessels[vessels < -500] = 0
          show_slice(vessels)
          if denoise:
               return denoise_vessels(lungs_contour, vessels)
          show_slice(vessels)

          return vessels

     def split_array_coords(array, indx=0, indy=1):
          x = [array[i][indx] for i in range(len(array))]
          y = [array[i][indy] for i in range(len(array))]
          return x, y
     k=0
     for c, exam_path in enumerate(paths):
          k+=1
          img_name = exam_path.split("\\")[-1].split('.nii')[0]
          myFile = open(csv_path+'vessel_volumes_'+str(k)+'.csv', 'w')

          ct_img = nib.load(exam_path)
          pixdim = find_pix_dim(ct_img)
          ct_numpy = ct_img.get_fdata()

          n = ct_numpy.shape[2]
          if n%2==0:
               median = int(n/2)
          else:
               median = int(n/2) + 1
          
          median = median - int(median/4)
          l = median - 10
          r = median + 10
          for i in range(l,r+1):
          # for i in range(65,66):
               j = str(i)
               vessel_name = vessels + img_name + "_" + j +"_vessel_only_mask"
               overlay_name = overlay_path + img_name + "_" + j + "_vessels"
               # out_mask_name = outpath + img_name + "_" + j + "_mask"
               contour_name = contour_path + img_name + "_" + j + "_contour"
               ct_numpy = ct_img.get_fdata()
               ct_numpy = ct_numpy[:,:,i]
               contours = intensity_seg(ct_numpy, -1000, -300)

               lungs_contour = find_lungs(contours)
               show_contour(ct_numpy, lungs_contour, contour_name,save=True)
               lung_mask = create_mask_from_polygon(ct_numpy, lungs_contour)

               lung_area = compute_area(lung_mask, find_pix_dim(ct_img))

               vessels_only = create_vessel_mask(lung_mask, ct_numpy, denoise=True)

               overlay_plot(ct_numpy, vessels_only)
               # plt.title('Overlayed plot')
               # fig = plt.figure(facecolor = '#202020')
               plt.savefig(overlay_name,bbox_inches='tight')
               
               plt.close()

               save_nifty(vessels_only, vessel_name, affine=ct_img.affine)

               vessel_area = compute_area(vessels_only, find_pix_dim(ct_img))
               ratio = (vessel_area / lung_area) * 100
               print(img_name,i, 'Vessel %:', ratio)
               lung_areas_csv.append([img_name,i, lung_area, vessel_area, ratio])
               ratios.append(ratio)

     # Save data to csv file
          with myFile:
               writer = csv.writer(myFile)
               writer.writerows(lung_areas_csv)