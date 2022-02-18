import os
import SimpleITK as sitk
import numpy as np
'''
nii.gz .vtk 等数据之间的相互转化
'''




def load_vtk(vtk_path):
    vtk_image = sitk.ReadImage(vtk_path)
    numpy_image = sitk.GetArrayFromImage(vtk_image)
    numpy_origin = np.array(list(reversed(vtk_image.GetOrigin())))
    numpy_space = np.array(list(reversed(vtk_image.GetSpacing())))

    return numpy_image, numpy_origin, numpy_space

def save_nii(numpy_image,origin, space, nii_path):
    if type(origin) == list:
        origin = tuple(reversed(origin))
    else:
        origin = tuple(reversed(origin.tolist()))
    if type(space) == list:
        space = tuple(reversed(space))
    else:
        space = tuple(reversed(space.tolist()))
    itk_image = sitk.GetImageFromArray(numpy_image)
    itk_image.SetSpacing(space)
    itk_image.SetOrigin(origin)
    sitk.WriteImage(itk_image, nii_path, True)


def vtk2nii(vtk_path, nii_dir):
    numpy_image, numpy_origin, numpy_space = load_vtk(vtk_path)
    if not os.path.exists(nii_dir):
        os.makedirs(nii_dir)
    data_name = os.path.split(vtk_path)[1]
    if data_name.endswith('.vtk'):
        nii_name = data_name.replace('.vtk', '.nii.gz')
    # elif data_name.endswith('.nii.gz'):
    #     nii_name = data_name.replace('.nii.gz', '.vtk')
    else:
        print ("checkout data")
        exit()
    # nii_name = os.path.split(vtk_path)[1].replace( '.nii.gz','.vtk')
    nii_path = os.path.join(nii_dir, nii_name)
    save_nii(numpy_image, numpy_origin, numpy_space, nii_path)