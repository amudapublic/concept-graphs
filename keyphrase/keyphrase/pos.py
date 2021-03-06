#Sample command: python pos.py ds8.txt "/usr/share/red5/webapps/oflaDemo/transcripts" "/var/www/metadata/output/preprocess_audio" enable "Porter-Stemmer"

import sys
import nltk
import os
import subprocess
import math
from operator import itemgetter
from time import gmtime, strftime
from nltk import stem
from nltk.stem.wordnet import WordNetLemmatizer
import subprocess

global stemmer_name
global file_name
global pos_status
global input_folder
global output_folder
global tagged_file_ext
global untagged_file_ext
global stem_to_root
#global stemmer
stem_to_root={}

try:
	file_name=sys.argv[1]
	input_folder="transcript"
	output_folder="output"
	stemmer_name=sys.argv[2]
	pos_status=sys.argv[3]
	tagged_file_ext="_tagged.txt"
	untagged_file_ext="_untagged.txt"
	print file_name
	print pos_status
	print stemmer_name
	print input_folder
	print output_folder
except:
	print "Mandatory parameters not available"
	sys.exit()

def stem_token(token):
	root_word=token
	print "inside"
	if stemmer_name=="Porter-Stemmer":
		print ("Performing Porter Stemming")
		stemmer = stem.PorterStemmer()
		token=stemmer.stem(token)
	elif stemmer_name=="Lancaster-Stemmer":
		print ("Performing Lancaster Stemming")
		stemmer = stem.LancasterStemmer()
		token=stemmer.stem(token)
	elif stemmer_name=="WordNet-Lemmatizer":
		print ("Performing Wordnet Lemmatization")
		stemmer = WordNetLemmatizer()
		token=stemmer.lemmatize(token)
		print token
	stem_to_root[token]=root_word
	return(token)

def preprocess(token):
		token=token.lower()
		token=token.rstrip(".")
		#token=token.rstrip("'s")
		token=token.rstrip(",")
		token=token.rstrip(")")
		token=token.lstrip("(")
		token=token.lstrip("{")
		token=token.rstrip("}")
		token=token.lstrip("[")
		token=token.rstrip("]")
		token=token.rstrip(":")
		token=token.rstrip("-")
		if stemmer_name!=None:
			token=stem_token(token)
		 #print "executing stemmer"
			#token=stemmer.stem(token)
		return token

def find_pos(content_tokens):
	content_with_tag=[]
	if pos_status=="enable":
		content_with_tag=nltk.pos_tag(content_tokens)
		#print content_with_tag[0];
		#print type(content_with_tag[0])
	else:
		i=0
		#content_with_tag=[]
		for c in content_tokens:
			content_with_tag.append((c,'NONE'))
			i+=1
	return content_with_tag

def write_to_file(content_with_tag):
	lecture_name=file_name.split(".")[0]
	#tag_file=tag_file.split("/")[1]
	untag_file=output_folder+"/"+lecture_name+untagged_file_ext
	tag_file=output_folder+"/"+lecture_name+tagged_file_ext	
	tg=open(tag_file,"w")
	tug=open(untag_file,"w")
	for w1,t1 in content_with_tag:
		main_word=w1
		w1=preprocess(w1)
		tg.write(w1+"/"+t1+"/"+main_word+" ")
		tug.write(w1+" ")
	tg.close()
	tug.close()
	#command='chmod 777 '+tag_file
	#subprocess.call(['chmod 777 '+tag_file])
	os.system('chmod 777 '+tag_file)
	os.system('chmod 777 '+untag_file)
	
def write_stem_to_root(stem_to_root):
	lecture_name=file_name.split(".")[0]
	root_file=output_folder+"/"+lecture_name+"_root.txt"
	rhandle=open(root_file,"w")
	for r in stem_to_root.keys():
		rhandle.write(r+"::"+stem_to_root[r]+"\n")
	rhandle.close()

#content = subprocess.Popen(["antiword",d],stdout=subprocess.PIPE).stdout.read()
#print 
r_txt=open(input_folder+"/"+file_name,"r")
content=r_txt.read()
content_tokens=nltk.word_tokenize(content.lower())
content_with_tag=find_pos(content_tokens)
write_to_file(content_with_tag)	
if stemmer_name!="none":
	write_stem_to_root(stem_to_root)
	
