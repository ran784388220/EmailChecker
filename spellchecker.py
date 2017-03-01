from os import listdir
import os
import sys
import string
import shutil
import math
from decimal import *

def makedictionary(spam_directory, ham_directory, dictionary_filename):
	dic_spam = {}
	dic_ham = {}
	dictionary_list = {}
	temp = []
	dic_spam = read_ham_spam_file(spam_directory)
	dic_ham = read_ham_spam_file(ham_directory)
	key_spam = dic_spam.keys()
	create_dictionary_file = open(dictionary_filename, 'a')
	for item in key_spam:
		if dic_ham.has_key(item):
			prob_ham = Decimal(dic_ham[item])/len(dic_ham.keys())
			prob_spam = Decimal(dic_spam[item])/len(dic_spam.keys())
			temp = [myformat(float(prob_ham)), myformat(float(prob_spam))]
			dictionary_list[item] = temp
			line = item + " "+temp[0]+" "+temp[1] + "\n"
			print line
			create_dictionary_file.write(line)
	create_dictionary_file.close()
def  myformat(x):
	return ('%.6f'%x).rstrip('0').rstrip('.')

#open the file and filter and save it in a list	
def file_list(email_directory):
	bad_words=["From","Return-Path:","Received:","Delivered-To:","To:","Cc:","References:","In-Reply-To:","List-Unsubscribe:","List-Post:","List-Help:","List-Id:"]
	email_list = []
	with open(email_directory) as oldfile:
		for line in oldfile:
			if not any(bad_word in line for bad_word in bad_words):
			 	email_list.append(line)
	email_after_filter=filter_email(email_list)
	return email_after_filter

#create the dictionary of spam/ham
def read_ham_spam_file(email_directory):
	dic = {}
	bad_words=["From","Return-Path:","Received:","Delivered-To:","To:","Cc:","References:","In-Reply-To:","List-Unsubscribe:","List-Post:","List-Help:","List-Id:"]
	email_list = []
	x = []
	c = listdir(email_directory)
	for i in c:
		file_string=""
		file_string=email_directory+"/"+i
		email_list = file_list(file_string)
		x.extend(email_list)
	for k in x:
		temp = x.count(k)
		dic[k] = temp  
	return dic
# filtering the file
def filter_email(email_list):
	#remove from: return: received:
	remove_header = ""
	result=""
	remove_header=''.join(str(e) for e in email_list)
	#remove all the numbers and replace punctuations with space,'\t','\n'
	filter_num=''.join([i for i in remove_header if not i.isdigit()])
	for c in string.punctuation:
		filter_num=filter_num.replace(c," ")	
	filter_num=filter_num.strip()
	filter_num=''.join([line for line in filter_num.split('\n') if line.strip()!=' '])
	filter_num=filter_num.replace("\t",'')
	filter_num=filter_num.lower()
	filter_num="".join(c for c in filter_num if 0<ord(i)<128)
	words = filter_num.split(" ")
	#filter duplicate words
	words=set(words)
	final=[]
	for x in filter(None,words):
		final.append(x)
	return final

def spamsort(mail_directory, spam_directory, ham_directory, dictionary, spam_prior_probability):
	c = listdir(mail_directory)
	comp_ham = 0
	comp_spam = 0
	temp_mail = []
	dict = {}
	dic = {}
	file_dic = open(dictionary)
	while 1:
		line = file_dic.readline()
		if not line:
			break
		row = line.split(" ")
		dict[row[0]] =[float(row[1]), float(row[2])]
	dic =  dict
	print len(c)
	for i in c:

		temp = file_list(mail_directory+"/"+i)
		print (mail_directory+"/"+i)
		# mail_dic = read_ham_spam_file(temp)
		# dic_items=mail_dic.keys()
		for item in temp:
			final1 = 0
			final2 = 0
			if dic.has_key(item):
				comp_ham = comp_ham + math.log(dic[item][0],2)
				comp_spam = comp_spam + math.log(dic[item][1],2)
		final1 = comp_ham + math.log((1-spam_prior_probability),2)#ham
		final2 = comp_spam + math.log(spam_prior_probability,2)
		comp_ham = 0
		comp_spam = 0
		print final1, final2
		if(final1<final2):
			print "move to ham"
		else:
			print "move to spam"
		if (final1<final2):
			src0 = mail_directory+"/"+i
			dst0 = ham_directory
			shutil.move(src0,dst0)
		else :
			src1 = mail_directory+"/"+i
			dst1 = spam_directory
			shutil.move(src1,dst1)
		
# read dictionary file and output as dictionary python format
# def read_dictionary(dictionary_file):
# 	dict = {}
# 	file_dic = open(dictionary_file)
# 	while 1:
# 		line = file_dic.readline()
# 		if not line:
# 			break
# 		row = line.split(" ")
# 		dict[row[0]] =[float(row[1]), float(row[2])]
# 	return dict
	
def main():
	s = "easy_ham"
	h = "spam"
	d = "dictionary"
	mail_directory="check_folder"
	
	prob = 0.3
	makedictionary(s, h, d)
	if not os.path.exists("spam_folder"):
		os.makedirs("spam_folder")
	if not os.path.exists("ham_folder"):
		os.makedirs("ham_folder")
	spam="spam_folder"
	ham = "ham_folder"
	spamsort(mail_directory,spam,ham,d,prob)
if __name__ == "__main__":
	main()