import os.path

IMAGE_PATHS = [ 
                'D:\\ML\\hot\\Datasets\\all_annotatedFrames_crop',
                'Z:\\PUC-Rio\\doutorado\\Imagens Medicas\\all_annotatedFrames_crop',
                'C:\\Projetos\\ml\\datasets\\all_annotatedFrames_crop',
                'D:\\Gusmao\\Tecgraf\\Deep_Learning\\all_annotatedFrames_crop',
                ''
              ]

def get_first_existing_path(paths):

    for path in paths:
        if (os.path.isabs(path) == False):
            path = os.path.abspath(path)

        if (os.path.isdir(path) == True):
            return path

    return None

def get_images_path():
    return get_first_existing_path(IMAGE_PATHS)
