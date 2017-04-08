#Searching and Downloading Google Images/Image Links
#https://github.com/hardikvasa/google-images-download/blob/master/google-images-download.py

#pip3 install numpy
#pip3 install Pillow
#pip3 install -U scikit-image
#to run: python3 genart.py

import time
import sys
import urllib.request
import numpy as np
from PIL import Image
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError
import priorityQueue
import itertools
# from multiprocessing import Pool
# from functools import partial
from skimage.measure import compare_ssim as ssim

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    lst1 = list(imageA.getdata())
    lst1_flattened = list(itertools.chain(*lst1))

    lst2 = list(imageB.getdata())
    lst2_flattened = list(itertools.chain(*lst2))
    if len(lst1_flattened) != len(lst2_flattened):
        # print('error')
        return 0
    res = (np.array(lst1_flattened) - np.array(lst2_flattened)) ** 2
    # print(res)
    err = np.sum(res)
    err /= float(imageA.size[0] * imageA.size[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info

    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        # import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = Request(url, headers = headers)
            resp = urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        # from urllib.request
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = Request(url, headers = headers)
            response = urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


############## Main Program ############
def prelim():
    t0 = time.time()   #start the timer

    #Download Image Links
    items = []
    search = ""
    #not using keywords
    for keyword in search_keyword:
        pure_keyword = keyword.replace(' ','%20')
        search += pure_keyword

    url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    raw_html =  (download_page(url))
    time.sleep(0.1)
    items = (_images_get_all_items(raw_html))
    #print ("Image Links = "+str(items))
    print ("Total Image Links = "+str(len(items)))
    print ("\n")


    #This allows you to write all the links into a test file. This text file will be created in the same directory as your code. You can comment out the below 3 lines to stop writing the output to the text file.
    # info = open('output.txt', 'a')        #Open the text file called database.txt
    # info.write(str(i) + ': ' + str(search_keyword[i-1]) + ": " + str(items) + "\n\n\n")         #Write the title of the page
    # info.close()                            #Close the file

    t1 = time.time()    #stop the timer
    total_time = t1-t0   #Calculating the total time required to crawl, find and download all the links of 60,000 images
    print("Total time taken: "+str(total_time)+" Seconds")
    print ("Starting Download...")

    ## To save imges to the same directory
    # IN this saving process we are just skipping the URL if there is any error

    k=0
    errorCount=0
    while(k < min(5, len(items))):
        try:
            req = Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req)
            output_file = open(str(k+1) + ".jpg","wb")
            data = response.read()
            output_file.write(data)
            response.close();
            image = Image.open(str(k+1)+".jpg")
            images[str(k+1)+".jpg"] = image
            print("completed ====> "+str(k+1))
            k=k+1;
        except IOError:   #If there is any IOError
            errorCount+=1
            print("IOError on image "+str(k+1))
            k=k+1;
        except HTTPError as e:  #If there is any HTTPError
            errorCount+=1
            print("HTTPError"+str(k))
            k=k+1;
        except URLError as e:
            errorCount+=1
            print("URLError "+str(k))
            k=k+1;

    print("\n")
    print("All are downloaded")
    print("\n"+str(errorCount)+" ----> total Errors")

def computeSimilarity(orig_image, images):
    running_sum = 0
    for imageName in images.keys():
        image = images[imageName]
        orig_image_size = orig_image.size
        running_sum += mse(orig_image, image.resize(orig_image_size))
        # lst1 = list(orig_image.getdata())
        # lst1_flattened = list(itertools.chain(*lst1))
        # # lst1_flattened = np.array(lst1_flattened)
        # lst2 = list(image.resize(orig_image_size).getdata())
        # lst2_flattened = list(itertools.chain(*lst2))
        # lst2_flattened = np.array(lst2_flattened)
        # running_sum += ssim(lst1_flattened, lst2_flattened)
    print("computed similarity")
    return running_sum / len(images.keys())

def create_collage(width, height, listofimages):
    cols = 3
    rows = 1
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []
    for p in listofimages:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            print(i, x, y)
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0

    new_im.save("Collage.jpg")


if __name__ == '__main__':
    #This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
    oi = input("Enter your object of interest: ")
    adj1 = input("Adjective 1: ")
    search_keyword = [oi]
    # pool = Pool(processes=6)
    images = {}
    pq = priorityQueue.PriorityQueue()
    #This list is used to further add suffix to your search term. Each element of the list will help you download 100 images. First element is blank which denotes that no suffix is added to the search keyword of the above list. You can edit the list by adding/deleting elements from it.So if the first element of the search_keyword is 'Australia' and the second element of keywords is 'high resolution', then it will search for 'Australia High Resolution'
    keywords = ["high resolution", "Blue"]
    prelim()
    for imageName in images.keys():
        image = images[imageName]
        pq.update(imageName, computeSimilarity(image, images))
        # args.append(image)
        # order.append(imageName)

    # partial_harvester = partial(computeSimilarity, images=images)
    # result_similarities = pool.map(partial_harvester, args, 1)
    # pool.close()
    # pool.join()

    # assert len(order) == len(args)
    # for i in range(len(order)):
    #     imageName = order[i]
    #     similarity = result_similarities[i]
    #     pq.update(imageName, similarity)
    order = []
    for i in range(3):
        imageName = pq.pop()[1]
        print(i, " : ", imageName)
        order.append(imageName)
        # image = Image.open(imageName)
        # image.show()

    create_collage(450, 300, order)
    image = Image.open("Collage.jpg")
    image.show()

#idea: get top 10 best representative images for the search query based on similarity with the
#100 responses, then make a collage of these with biggest representing best, smallest representing worst

#----End of the main program ----#
