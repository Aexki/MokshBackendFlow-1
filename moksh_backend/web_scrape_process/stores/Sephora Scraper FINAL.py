#!/usr/bin/env python
# coding: utf-8

# In[62]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# In[79]:


class SephoraScrapper:
    def __init__(self):
        self.driver = None
        
    def openWindow(self, link):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--auto-open-devtools-for-tabs")

        self.driver = webdriver.Chrome(r"chromedriver.exe", options = options)

        self.driver.get(link)

        for val in range(500, 3001, 300):
            self.driver.execute_script(f"""window.scrollTo(0, {val})""")
            time.sleep(0.5)
        
        self.driver.execute_script(f"""window.scrollTo(0, 0)""")
        print("Page loaded successfully")
    
    def jumpToPage(self, pageNumber):
        pgCount = 1
        while pgCount <= pageNumber:
            self.nextPage()
            pgCount += 1
    
    def scrollToReviews(self):
        for val in range(500, 3801, 300):
            self.driver.execute_script(f"""window.scrollTo(0, {val})""")
            time.sleep(1)
    
    def getLastPage(self):
        lastPage = 1
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "css-tu1ert")))
            for ele in self.driver.find_elements_by_class_name("css-tu1ert"):
                print(ele.text)
                if ele.text.isdigit():
                    lastPage = max(lastPage, int(ele.text))
        except TimeoutException:
            print("No Last Page")
        return lastPage
    
    def nextPage(self):
        for x in range(4000,9000,250):
            try :
                self.driver.execute_script(f"""window.scrollTo(0, {x})""")
                self.driver.find_element_by_class_name("css-140qkrj").click()
                time.sleep(3)
                break
            except ElementClickInterceptedException as ex:
                continue
            except NoSuchElementException as e:
                continue
            except StaleElementReferenceException as e:
                continue
    
    def getReviews(self):
        pgCount = 1
        lastPage = self.getLastPage()
        recordList = []
        while pgCount <= lastPage:
            print('Running on ', pgCount)
            try:
                elements = self.driver.find_elements_by_class_name("css-dfftxd")
                for element in elements:
                    try:
                        rating = element.find_element_by_class_name("css-mu0xdx").get_attribute('aria-label')
                    except Exception as e:
                        print(e)

                    try:
                        verified = element.find_element_by_class_name("css-gtt1cr").text
                        verified = 'Yes'
                    except Exception as e:
                        verified = 'No'

                    try:
                        date = element.find_element_by_class_name("css-1m76p7e").text
                    except Exception as e:
                        print(e)

                    try:
                        review_title = element.find_element_by_class_name("css-m9drnf").text
                    except Exception as e:
                        review_title = ''

                    try:
                        product_shade = element.find_element_by_class_name("css-hoe9xz").text
                    except Exception as e:
                        product_shade = ''

                    try:
                        review = element.find_element_by_class_name("css-k7hahd").text
                    except Exception as e:
                        review = ''

                    try:
                        recommended = element.find_element_by_class_name("css-12com3g").text
                        recommended = 'Yes'
                    except Exception as e:
                        recommended = 'No'

                    try:
                        votes = element.find_element_by_class_name("css-1ds6ck2").text
                        votes = votes.splitlines()
                        upvote = votes[1].replace('(','').replace(')','')
                        downvote = votes[3].replace('(','').replace(')','')
                    except Exception as e:
                        upvote = '0'
                        downvote = '0'

                    try:
                        reviewer = element.find_element_by_class_name("css-11cofee").text
                    except Exception as e:
                        reviewer = ''

                    try:
                        reviewer_des = element.find_element_by_class_name("css-2h4ti5").text
                    except Exception as e:
                        reviewer_des = ''

                    try:
                        incentivized = element.find_element_by_class_name("css-ezht25").text
                        incentivized = 'Yes'
                    except Exception as e:
                        incentivized = 'No'

                    recordList.append({'Date':date,'Verified Purchase': verified, 'Recommended': recommended, 
                                       'Incentivized': incentivized, 'Product shade': product_shade, 'Rating': rating, 
                                       'Review Title': review_title, 'Review': review, 'Upvote': upvote, 
                                       'Downvote': downvote, 'Reviewer Name': reviewer, 'Reviewer Description' : reviewer_des})
            except Exception as e:
                print(e)
                
            self.nextPage()

            pgCount += 1
            
        return recordList
    
    def scrapAndSaveReviews(self, fileName):
        self.scrollToReviews()
        recordList = self.getReviews()
        df = pd.DataFrame.from_dict(recordList, orient='columns')
        df.to_csv(fileName, index=False)
    
    def toggleDropdown(self, filterName):
        filterId = ''
        if filterName == "SkinConcerns":
            filterId = 'custom_skinConcerns_trigger'
        elif filterName == "AgeRange":
            filterId = 'custom_ageRange_trigger'
        
        for val in range(3000, 4101, 300):
            try:
                self.driver.execute_script(f"""window.scrollTo(0, {val})""")
                button = self.driver.find_element_by_id(filterId)
                time.sleep(1)
                button.click()
                return
            except ElementClickInterceptedException as ex:
                continue
    
    def getFilterTextList():
        self.toggleDropdown()
        filterList = self.driver.find_elements_by_class_name('css-z9tqly')
        filterTextList = [ele.text for ele in filterList if ele.text.strip() != ""]
        self.toggleDropdown()
        return filterTextList
    
    def applyFilter(self, value):
        if value == "clear":
            clearList = self.driver.find_elements_by_class_name('css-1ckos4y')
            for x in range(4000,5000,100):
                try :
                    self.driver.execute_script(f"""window.scrollTo(0, {x})""")
                    for ele in clearList:
                        if ele.text == "Clear":
                            ele.click()
                            time.sleep(1)
                            return
                except ElementClickInterceptedException as ex:
                    continue
                    
        elif value == "done":
            doneList = self.driver.find_elements_by_class_name('css-1fn544n')
            for x in range(4000,5000,100):
                try :
                    self.driver.execute_script(f"""window.scrollTo(0, {x})""")
                    for ele in doneList:
                        if ele.text == "Done":
                            ele.click()
                            time.sleep(2)
                            return
                except ElementClickInterceptedException as ex:
                    continue
        else:
            ageRangeList = self.driver.find_elements_by_class_name('css-z9tqly')
            for ele in ageRangeList:
                if ele.text == value:
                    ele.click()
                    time.sleep(1)
                    return
    
    def getSpecificFilter(self, filterName):
        if filterName not in ["AgeRange", "SkinConcerns"]:
            print("Not Implemented for filter - ", filterName)
            return

        filterTextList = getFilterTextList(filterName)
        resultList = []
        for filterValue in filterTextList:
            toggleDropdown()
            applyFilter("clear")
            applyFilter(filterValue)
            applyFilter("done")
            pgCount = 1
            lastPage = getLastPage()
            while pgCount <= lastPage:
                print('Running on ', pgCount, " out of ", lastPage, " for ", filterValue)
                try:
                    elements = self.driver.find_elements_by_class_name("css-dfftxd")
                    for element in elements:
                        try:
                            reviewer = element.find_element_by_class_name("css-11cofee").text
                        except Exception as e:
                            reviewer = ''
                        resultList.append({"Reviewer" : reviewer, filterName : filterValue})

                except Exception as e:
                    print(e)

                self.nextPage()

                pgCount += 1
                
    def scrapAndSaveSpecificFilter(self, filterName, fileName):
        self.scrollToReviews()
        recordList = self.getSpecificFilter(filterName)
        df = pd.DataFrame.from_dict(recordList, orient='columns')
        df.to_csv(fileName, index=False)
        
    def getProductInfo(self):
        self.driver.execute_script(f"""window.scrollTo(0, 500)""")
        
        brandName = self.driver.find_element_by_class_name("css-1gyh3op").text
        productName = self.driver.find_element_by_class_name("css-1pgnl76").text
        rating = self.driver.find_element_by_class_name("css-1tbjoxk").get_attribute('aria-label')
        noOfReviews = self.driver.find_element_by_class_name("css-1j53ife").text
        noOfHearts = self.driver.find_element_by_class_name("css-jk94q9").text
        
        imagesDiv = self.driver.find_element(By.CSS_SELECTOR, "div[data-comp='Carousel ']")
        imageLinks = list(map(lambda x : x.get_attribute('src'), imagesDiv.find_elements(By.TAG_NAME, "img")))
        imageLinks = list(filter(lambda link : "svg" not in link.lower() and "videoimage" not in link.lower(), imageLinks))
        
        sizeButtonClass = ["css-1sn75vo", "css-1tvsewh"]
        sizeNameClass = ["css-1a157mi", "css-15thuqz"]    

        sizeButtonElements = self.driver.find_elements_by_class_name(sizeButtonClass[0]) + self.driver.find_elements_by_class_name(sizeButtonClass[1])
        sizeNameElements = self.driver.find_elements_by_class_name(sizeNameClass[0]) + self.driver.find_elements_by_class_name(sizeNameClass[1])

        recordList = []

        i = 0
        j = 0
        for ele in self.driver.find_elements_by_class_name("css-1hdop86"):
            sizeNameText = sizeNameElements[i].text
            quantityText = list(filter(lambda x : True if x.strip() not in ["SALE", "NEW"] else False, ele.text.split("\n")))
            for text in quantityText:
                sizeButtonElements[j].click()
                time.sleep(2)
                defaultCostText = self.driver.find_element_by_class_name("css-18jtttk").text.split(" ")[0]
                recordList.append({"Brand Name" : brandName, "Product Name" : productName, "Avg Rating" : rating,
                                  "No of Reviews" : noOfReviews, "Likes" : noOfHearts,
                                  "Size" : sizeNameText, "Quantity" : text, "Cost" : defaultCostText, "Image Links" : imageLinks})
                j += 1
            i += 1
        
        if len(sizeButtonElements) == 0:
            quantityText = self.driver.find_element_by_class_name("css-7ihc3u").text.split("\n")[0].strip("Size ")
            sizeNameText = sizeNameElements[0].text
            defaultCostText = self.driver.find_element_by_class_name("css-18jtttk").text.split(" ")[0]
            recordList.append({"Brand Name" : brandName, "Product Name" : productName, "Avg Rating" : rating,
                              "No of Reviews" : noOfReviews, "Likes" : noOfHearts,
                              "Size" : sizeNameText, "Quantity" : quantityText, "Cost" : defaultCostText, "Image Links" : imageLinks})

        return recordList[0]
    
    def scrapAndSaveProductInfo(self, fileName):
        recordList = self.getProductInfo()
        df = pd.DataFrame.from_dict(recordList, orient='columns')
        df.to_csv(fileName, index=False)
    
    def getSimilarProducts(self):
        for val in range(500, 2801, 300):
            self.driver.execute_script(f"""window.scrollTo(0, {val})""")
            time.sleep(0.5)

        parent_class = "css-wqvm28"
        parent_element = self.driver.find_element_by_class_name(parent_class)

        similar_prod_class = "css-145rinu"
        similar_prods = parent_element.find_elements_by_class_name(similar_prod_class)

        prod_link_class = "css-unapqu"
        image_class = "css-1rovmyu"
        comapny_name_class = "css-262lw8"
        prod_name_class = "css-kzorxn"
        prod_cost_class = "css-7i38uj"
        fill_size_class = "css-kzorxn eanm77i0"
        rating_class = "css-1tbjoxk" #get aria-label
        review_class = "css-1dk1ux" #get aria-label
        ingredient_highlights = "css-12n2qsi"

        company_ls = []
        image_ls = []
        name_ls = []
        link_ls = []
        cost_ls = []
        fill_ls = []
        rating_ls = []
        review_ls = []
        ingredients_ls = []

        for prod in similar_prods:
            try:
                link = prod.find_element_by_class_name(prod_link_class).get_attribute('href')
                link_ls.append(link)
            except Exception as e:
                print(e)
                print("Prod link - Test failed")

            try:
                image = prod.find_element(By.CSS_SELECTOR, "img[data-comp='Image StyledComponent BaseComponent ']").get_attribute('src')
                image_ls.append(image)
            except Exception as e:
                print("Image - Test Failed")

            try:
                company = prod.find_element_by_class_name(comapny_name_class).text
                company_ls.append(company)
            except Exception as e:
                print(e)
                print("Company - Test failed")

            try:
                name = prod.find_element_by_class_name(prod_name_class).text
                name_ls.append(name)
            except Exception as e:
                print(e)
                print("Name - Test failed")

            try:
                cost = prod.find_element_by_class_name(prod_cost_class).text
                cost_ls.append(cost)
            except Exception as e:
                print(e)
                print("Cost - Test failed")

            try:
                rating = prod.find_element_by_class_name(rating_class).get_attribute('aria-label')
                rating_ls.append(rating)
            except Exception as e:
                print(e)
                print("Rating - Test failed")

            try:
                review = prod.find_element_by_class_name(review_class).text
                review_ls.append(review)
            except Exception as e:
                print(e)
                print("Review - Test failed")

            try:
                complex_ele = prod.find_elements_by_class_name(ingredient_highlights)
                fill_ls.append(complex_ele[1].text)
                ingredients_ls.append(complex_ele[3].text)
            except Exception as e:
                print(e)
                print("Ingredients and fill size - Test failed")

        similarProducts = [{'Product Link': link_ls[i],
                            'Product Image' : image_ls[i],
                            'Brand Name': company_ls[i], 
                            'Product Name': name_ls[i], 
                            'Rating': rating_ls[i], 
                            'Review': review_ls[i],
                            'Cost': cost_ls[i], 
                            'Fill Size': fill_ls[i], 
                            'Ingredients': ingredients_ls[i]} for i in range(len(company_ls))]
        
        self.driver.find_elements(By.CSS_SELECTOR, "a[class='css-sdfa4l eanm77i0']")[-1].click()
        
        for val in range(300, 3000, 300):
            self.driver.execute_script(f"""window.scrollTo(0, {val})""")
            time.sleep(0.5)

        self.driver.execute_script(f"""window.scrollTo(0, 100)""")

        div_tags = self.driver.find_elements(By.CSS_SELECTOR, "a[class='css-klx76']")
        searchResults = []

        for card in div_tags:
            try:
                searchResults.append({"Product Link" : card.get_attribute('href'),
                                      "Product Image" : card.find_element(By.CSS_SELECTOR, "img[class='css-1rovmyu eanm77i0']").get_attribute('src'),
                                      "Brand Name" : card.find_element(By.CSS_SELECTOR, "span[class='css-bpsjlq eanm77i0']").text,
                                      "Product Name" : card.find_element(By.CSS_SELECTOR, "span[class='ProductTile-name css-h8cc3p eanm77i0']").text,
                                      "Rating" : card.find_element(By.CSS_SELECTOR, "span[class='css-mu0xdx']").get_attribute('aria-label'),
                                      "Review" : card.find_element(By.CSS_SELECTOR, "span[class='css-qbbayi']").text,
                                      "Cost" : card.find_element(By.CSS_SELECTOR, "b[class='css-1f35s9q']").text,
                                     })
            except NoSuchElementException:
                pass

        for resultSet in searchResults:
            if 'K' in resultSet["Review"]:
                resultSet["Review"] = float(resultSet["Review"][:-1])*1000
            else:
                resultSet["Review"] = float(resultSet["Review"])
        
        for resultSet in similarProducts:
            if 'K' in resultSet["Review"]:
                resultSet["Review"] = float(resultSet["Review"][:-1])*1000
            else:
                resultSet["Review"] = float(resultSet["Review"])
                
        return similarProducts + sorted(searchResults, key = lambda x : -x["Review"])[:5]

    def closeWindow(self):
        self.driver.quit()

