import pdfquery
from pdfquery import *
import codecs
from unidecode import unidecode
import re,time

t1 = time.time()
my_list = []

for page_num in range(2,46) :

	row = 10 ; col = 3
	x0 = 15 ; x1 = 203 ; y0 = 707 ; y1 = 779

	pdf = pdfquery.PDFQuery("pdf_file.pdf")
	pdf.load(page_num)

	for i in range(col) :

		for j in range(row) :

			coords = str(x0)+","+str(y0)+","+str(x1)+","+str(y1)	
			# print coords
			parsed_text = pdf.pq('LTTextLineHorizontal:in_bbox("%s")'%(coords)).text()
			parsed_text = re.sub(" +"," ", parsed_text)
			uni_parsed_text = unidecode(unicode(parsed_text))
			uni_parsed_text = re.sub(" +"," ", uni_parsed_text)
			# print unidecode(unicode(parsed_text)),"\n"

			if 'mlpg' in uni_parsed_text and 'aadk' in uni_parsed_text :
				
				dic = {}
				
				temp_li_uni = uni_parsed_text.split(" ")
				temp_li = parsed_text.split(" ")
				
				try :
					name = temp_li[temp_li_uni.index('npm')+2:temp_li_uni.index('vptp')]

					dic['name'] = ' '.join(name)
					# print dic
				except :
					name = temp_li[temp_li_uni.index('npm')+2:temp_li_uni.index('pnt')]

					dic['name'] = ' '.join(name)

				temp_li_uni.pop(temp_li_uni.index('npm'))
			
				if 'pnt' in uni_parsed_text : 
					
					husband_name = temp_li[temp_li_uni.index('npm')+3:temp_li_uni.index('mkpn')+1]

					husband_name = ' '.join(husband_name)
					dic['husband_name'] = husband_name.strip()
					# print dic
				
				elif 'vptp' in uni_parsed_text : 					
					father_name = temp_li[temp_li_uni.index('npm')+3:temp_li_uni.index('mkpn')+1]
					
					father_name = ' '.join(father_name)
					dic['father_name'] = father_name.strip()

				# print dic
				house_num = temp_li_uni[temp_li_uni.index('spkhdp')+2:temp_li_uni.index('spkhdp')+3]
				house_num = ''.join(house_num)
				dic['house_num'] = house_num.strip()
				# print dic

				sex = temp_li[temp_li_uni.index('mlpg')+3:temp_li_uni.index('mlpg')+4]
				sex = ''.join(sex)

				if unidecode(unicode(sex)) == 'pkrss':
					dic['sex'] = "Male"
				else :
					dic['sex'] = "Female"
				# print dic
				temp_li_uni.pop(temp_li_uni.index('spkhdp')+2)
				# print temp_li_uni
				for itm in temp_li_uni :
					try :
						itm = int(itm.strip())
						dic['age'] = str(itm)
					except :
						pass

				for itm in temp_li_uni :
					
					if itm[0].isupper() :
						dic['ID'] = str(itm).strip()

				if 'husband_name' in dic.keys() :
		
					s = dic['ID']+","+dic['name']+","+dic['age']+","+dic['sex']+","+dic['house_num']+","+"NONE"+","+dic['husband_name']
					my_list.append(s)
				
				else:
		
					s = dic['ID']+","+dic['name']+","+dic['age']+","+dic['sex']+","+dic['house_num']+","+dic['father_name']+","+"NONE"
					my_list.append(s)

			y0 -= 72 ; y1 -= 72
		
		x0 += 188 ; x1 += 188
		
		y0 = 707 ; y1 = 779

	print "page : ",page_num

with codecs.open("names.csv", "w",encoding='utf-8') as file:
	file.writelines("ID,NAME,AGE,SEX,HOUSE NO.,FATHER'S NAME,HUSBAND'S NAME\n")
	file.writelines( "%s\n" % item for item in my_list )
t2 = time.time()
print t2-t1