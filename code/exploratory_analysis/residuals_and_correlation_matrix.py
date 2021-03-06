"""sub011, task001_run_001"""

import project_config
import nibabel as nib
import numpy as np 
import outliers_utils
import matplotlib.pyplot as plt
import numpy.linalg as npl
from scipy import stats
from stimuli_revised import events2neural_rounded

"""
Replace these variables before running the script
"""
BOLD_file_1 = '/Users/Lynn/Desktop/STAT259/project/ds115_sub010-014/sub010/BOLD/task001_run001/bold.nii.gz'
cond_filename = "/Users/Lynn/Desktop/STAT259/project/ds115_sub010-014/sub010/model/model001/onsets/task001_run001/cond002.txt"
conv_data_filename = 'results/conv_data.txt'


#loading data
img = nib.load(BOLD_file_1)
data = img.get_data() 
ds1 = data.shape
#drop the first five
data = data[..., 5:]
ds2 = data.shape
print("1.The original data shape is %r. After dropping the first five, now the data has the shape %r") %(str(ds1),str(ds2))

#standard deviations of all voxels along the TRs.
std = outliers_utils.vol_std(data)
fobj = open('results/vol_std_values.txt', 'wt')
for i in std:
	fobj.write(str(i) + '\n')
fobj.close()
print("2. The standard deviations of all voxels along the TRs are saved in to 'vol_std_values.txt'")

#find the std outliers
outlier = outliers_utils.iqr_outliers(std)[0]
fobj = open('results/vol_std_outliers.txt', 'wt')
for i in outlier:
	fobj.write(str(i) + '\n')
fobj.close()
print("3.There are %d std outliers, with indices %r. They are saved into 'vol_std_outliers.txt'") %(len(outlier),outlier)

#plot the std outliers
std_outlier=[]
low = outliers_utils.iqr_outliers(std)[1][0]
high = outliers_utils.iqr_outliers(std)[1][1]
for i in outlier:
	std_outlier.append(std[i])
x=np.arange(data.shape[-1])
std1, = plt.plot(x,std,'b',label="std values")
std2, = plt.plot(outlier,std_outlier,'ro',label="outliers")
lowbound = plt.axhline(y=low,color='r',ls='dashed',label='lower IRQ')
highbound = plt.axhline(y=high,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[std1, std2, lowbound,highbound],loc=4)
plt.ylabel('standard deviation')
plt.xlabel('volumns')
plt.title('Outliers Detection')
plt.savefig('results/vol_std.png')
plt.show()
print("The std outliers is plotted and saved as 'vol_std.png'")

#RMS diffrence
rms = outliers_utils.vol_rms_diff(data)
rms_outlier = outliers_utils.iqr_outliers(rms)[0]
rms_outlier_value = []
for i in rms_outlier:
	rms_outlier_value.append(rms[i])
low_rms = outliers_utils.iqr_outliers(rms)[1][0]
high_rms = outliers_utils.iqr_outliers(rms)[1][1]
xx = np.arange(len(rms))
plt.axis([0,140,0,25])
rms1, = plt.plot(xx,rms,'b',label="rms values")
rms2, = plt.plot(rms_outlier,rms_outlier_value,'ro',label="rms outliers")
lowbound_rms = plt.axhline(y=low_rms,color='r',ls='dashed',label='lower IRQ')
highbound_rms = plt.axhline(y=high_rms,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[rms1, rms2, lowbound_rms,highbound_rms],loc=1)
plt.ylabel('RMS difference')
plt.xlabel('indices')
plt.title('RMS difference outliers')
plt.savefig('results/vol_rms_outliers.png')
plt.show()
print("4.There are %d RMS outliers with indices %r.") %(len(rms_outlier),rms_outlier)
print("5.The RMS difference outliers is plotted and saved as 'vol_rms_outliers.png'")

#extended RMS outliers
ext_outlier = outliers_utils.extend_diff_outliers(rms_outlier)
rms.append(0)
ext_outlier_value = []
for i in ext_outlier:
	ext_outlier_value.append(rms[i])
low_ext = outliers_utils.iqr_outliers(rms)[1][0]
high_ext = outliers_utils.iqr_outliers(rms)[1][1]
xxx = np.arange(len(rms))
plt.axis([0,140,0,25])
ext1, = plt.plot(xxx,rms,'b',label="rms values")
ext2, = plt.plot(ext_outlier,ext_outlier_value,'ro',label="extended outliers")
lowbound_ext = plt.axhline(y=low_ext,color='r',ls='dashed',label='lower IRQ')
highbound_ext = plt.axhline(y=high_ext,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[ext1, ext2, lowbound_ext,highbound_ext],loc=1)
plt.ylabel('RMS difference')
plt.xlabel('volumns')
plt.title('Extended RMS difference outliers')
plt.savefig('results/extended_vol_rms_outliers.png')
plt.show()
fobj = open('results/extended_vol_rms_outliers.txt', 'wt')
for i in ext_outlier:
	fobj.write(str(i) + '\n')
fobj.close()
print("6.There are %d RMS exteded outliers with indices %r.They are saved into 'extended_vol_rms_outliers.txt'") %(len(ext_outlier),ext_outlier)
print("The RMS difference outliers is plotted and saved as'extended_vol_rms_outliers.png'")

#drop the outliers
rms = outliers_utils.vol_rms_diff(data)
rms_outlier = outliers_utils.iqr_outliers(rms)[0]
ext_outlier = outliers_utils.extend_diff_outliers(rms_outlier)
mask = np.ones(data.shape[-1])
mask[ext_outlier] = 0
mask = np.array(mask, dtype=bool)
data_rem=data[..., mask]
print("7.After dropping the extended RMS outliers, now the data has the shape %r.") %str(data_rem.shape)
 
#basic statistics
np.amin(data_rem) #0
np.amax(data_rem) #1550
np.mean(data_rem) #137.08845107920848

#get the correlation matrix w/ outliers
TR=2.5
n_trs = img.shape[-1]
time_course = events2neural_rounded(cond_filename, 2.5, n_trs) 
plt.plot(time_course)
plt.title("time_course")
plt.savefig("results/time_course.png")
plt.show()
print("8.The time_course is plotted and saved as 'time_course.png'")
time_course=time_course[5:]
correlations = np.zeros(data.shape[:-1])
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        for k in range(data.shape[2]):
            vox_values = data[i, j, k]
            correlations[i, j, k] = np.corrcoef(time_course, vox_values)[1, 0]
plt.imshow(correlations[:, :, 18], cmap='gray')
plt.colorbar()
plt.savefig("results/correlation_middle.png")
plt.title("Middle slice of correlations")
plt.show()
print("9.The middle slice of the third axis from the correlations array w/ outliers is plotted and saved as 'correlation_middle.png'")




#get the correlation matrix w/o the outliers

time_course_rem = time_course[mask]
correlations_rem = np.zeros(data_rem.shape[:-1])
for i in range(data_rem.shape[0]):
    for j in range(data_rem.shape[1]):
        for k in range(data_rem.shape[2]):
            vox_values_rem = data_rem[i, j, k]
            correlations_rem[i, j, k] = np.corrcoef(time_course_rem, vox_values_rem)[1, 0]
plt.imshow(correlations_rem[:, :, 18], cmap='gray')
plt.colorbar()
plt.savefig("results/correlation_middle_no_outliers.png")
plt.title("Middle slice of correlations without outliers")
plt.show()
print("10.The middle slice of the third axis from the correlations array without outliers is plotted and saved as 'correlation_middle_no_outliers.png'")

#residual analysis w/ outliers

convolved = np.loadtxt(conv_data_filename)
design = np.ones((len(convolved), 2))
design[:, 0] = convolved
data_2d = np.reshape(data, (-1, data.shape[-1]))
betas = npl.pinv(design).dot(data_2d.T)
y_hat=design.dot(betas)
vol_shape = data.shape[:-1]
n_voxels = np.prod(vol_shape)
voxel_by_time = np.reshape(data, (n_voxels, data.shape[-1]))
y=np.transpose(voxel_by_time)
residuals= y-y_hat
fobj = open('results/residuals.txt', 'wt')
for i in residuals:
	fobj.write(str(i) + '\n')
fobj.close()
print("11.the residuals are saved as 'residuals.txt'")
p_nor = []
for i in range(0,residuals.shape[-1]):
    p_nor.append(stats.shapiro(residuals[...,i])[1])
len(p_nor)
#for p<0.05, the voxel is not normal distributed
p_nor_005 = [i for i in p_nor if i < 0.05]
len(p_nor_005)
print("12.Before removing the outliers, there are %d voxels out of %d are not normally distributed." % (len(p_nor_005),len(p_nor)))

#residual analysis w/o outliers
design_rem = np.delete(design,ext_outlier,axis=0)
vol_shape_rem= data_rem.shape[:-1]
n_voxels_rem = np.prod(vol_shape_rem)
voxel_by_time_rem = np.reshape(data_rem, (n_voxels_rem, data_rem.shape[-1]))
y_rem=np.transpose(voxel_by_time_rem)

data_rem_2d = np.reshape(data_rem, (-1, data_rem.shape[-1]))
betas_rem = npl.pinv(design_rem).dot(data_rem_2d.T)
y_hat_rem = design_rem.dot(betas_rem)
residuals_rem = y_rem-y_hat_rem

fobj = open('results/residuals_no_outliers.txt', 'wt')
for i in residuals_rem:
    fobj.write(str(i) + '\n')
fobj.close()
print("13. the residuals with outliers dropped are saved as 'residuals_no_outliers.txt'")
p_nor_rem = []
for i in range(0,residuals_rem.shape[-1]):
    p_nor_rem.append(stats.shapiro(residuals_rem[...,i])[1])
len(p_nor_rem)
#for p<0.05, the voxel is not normal distributed
p_nor_rem005 = [i for i in p_nor_rem if i < 0.05]
len(p_nor_rem005)
print("14.After removing the outliers, there are %d voxels out of %d are not normally distributed." %(len(p_nor_rem005),len(p_nor_rem)))


#Since we are dealing with multiple comparison problems, here, we apply Bonferroni and Hochberg procedures to 
#adjust our false discovery rate (at level alpha).


"""
Bonferroni procedure:
reject the null if p < alpha/n where n is the sample size
"""
#with outliers 
p_bonf = [i for i in p_nor if i < 0.05/data.shape[-1]]
print("15.With Bonferroni correction, there are %d voxels out of %d are not normally distributed." % (len(p_bonf),len(p_nor)))

#without outliers
p_bonf_rem = [i for i in p_nor_rem if i < 0.05/data.shape[-1]]
print("16.With Bonferroni correction and outliers removed, there are %d voxels out of %d are not normally distributed." % (len(p_bonf_rem),len(p_nor_rem)))


"""
Hochberg's set up:
1. Order the p-values P(1),P(2),...,P(n) and their associated hypothesis H(1),...,H(n)
2. Reject all hypotheses H(k) having P(k) <= alpha/(n+1-k) where k=1,...,n

"""
# with outliers
p_nors = np.sort(p_nor)
alpha = 0.05
n=len(p_nors)
tf=[]
for i in range(0,len(p_nors)):
    thres = alpha/(n+1-(i+1))
    tf.append(p_nors[i]<=thres)
print("17.With Hochberg's procedure, there are %d voxels out of %d are not normally distributed." %(sum(tf),len(p_nors)))

# without outliers
p_nors_rem = np.sort(p_nor_rem)
alpha = 0.05
n=len(p_nors_rem)
tf=[]
for i in range(0,len(p_nors_rem)):
    thres = alpha/(n+1-(i+1))
    tf.append(p_nors_rem[i]<=thres)
print("17.With Hochberg's procedure and outliers removed, there are %d voxels out of %d are not normally distributed." %(sum(tf),len(p_nors_rem)))

""""
Benjamini-Hochberg procedure:
1. Order the p-values P(1),P(2),...,P(n) and their associated hypothesis H(1),...,H(n)
2. Reject all hypotheses H(k) having P(k) <= (k/n)*alpha where k=1,...,n

"""
#with outliers
tf=[]
for i in range(0,len(p_nors)):
    thres = (i/n)*alpha
    tf.append(p_nors[i]<=thres)
print("18.With Benjamini-Hochberg's procedure, there are %d voxels out of %d are not normally distributed." %(sum(tf),len(p_nors)))

#without outliers
tf=[]
for i in range(0,len(p_nors_rem)):
    thres = (i/n)*alpha
    tf.append(p_nors_rem[i]<=thres)
print("19.With Benjamini-Hochberg's procedure and outliers removed, there are %d voxels out of %d are not normally distributed." %(sum(tf),len(p_nors_rem)))



