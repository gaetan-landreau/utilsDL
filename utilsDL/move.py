import os
import argparse
import glob 
import shutil

class Move():
	def __init__(self,input_path,output_path):
		
		self.indir=input_path
		self.outdir=output_path
		
		# Get the list of ASIN code to process. 
		self.list_asin=self.get_ASIN_code()

		# Create a pandas dataframe for storing main info.
		self.df = RenameAmazonImgs.create_df()

		self.rename_all()

	def get_ASIN_code(self):
		asin_list=[]

		for dir in DIRECTORIES:
			raw_dirs=sorted(os.listdir(os.path.join(self.indir,'V'+str(self.version),dir)))
			asin_list.append([os.path.basename(l) for l in raw_dirs if not l.startswith('.')])	#Remove all hidden subfolders.
		
		# Ensure all sub dir before, after & sr has the exact same ASIN directories. 
		assert asin_list[0]==asin_list[1]
		assert asin_list[1]==asin_list[-1]
		assert asin_list[0]==asin_list[-1]

		return asin_list[0]
	@staticmethod
	def create_df():
		return pd.DataFrame(data={'IMG_IDX':[],'ASIN':[],'NB_CNTS_REMOVED':[],'DEFAULT':[]})
		

	@staticmethod
	def create_dirs(path):
		if not os.path.isdir(path):
			os.makedirs(path,exist_ok=False)
		

	def rename_inner_before(self,asin):

		out_path_asin = os.path.join(self.outdir,'V'+str(self.version),'before',asin)
		in_path_asin =  os.path.join(self.indir,'V'+str(self.version),'before',asin)

		RenameAmazonImgs.create_dirs(out_path_asin)

		old_basename_imgs_before=sorted(os.listdir(in_path_asin))

		self.nb_imgs_before=len(old_basename_imgs_before)
		idx=self.idx

		for old_basename_img in old_basename_imgs_before:

			new_basename_img='_'.join(['V'+str(self.version),asin,'1before','IMG'+str(idx).zfill(4)])+'.jpg'

			old_path_before=os.path.join(in_path_asin,old_basename_img)
			new_path_before=os.path.join(out_path_asin,new_basename_img)

			shutil.copy(old_path_before,new_path_before)

			idx+=1

	def rename_inner_after(self,asin):

		out_path_asin = os.path.join(self.outdir,'V'+str(self.version),'after',asin)
		in_path_asin =  os.path.join(self.indir,'V'+str(self.version),'after',asin)

		RenameAmazonImgs.create_dirs(out_path_asin)

		old_basename_imgs_after=sorted(os.listdir(in_path_asin), key=lambda x: int(x[-5]))	#Sort the named images by the last caracter. ; -5 to get the idx number just before the extension .jpg / .png

		self.nb_imgs_after=len(old_basename_imgs_after)
		idx=self.idx

		for old_basename_img in old_basename_imgs_after:

			new_basename_img='_'.join(['V'+str(self.version),asin,'2after','IMG'+str(idx).zfill(4)])+'.jpg'


			old_path_before=os.path.join(in_path_asin,old_basename_img)
			new_path_before=os.path.join(out_path_asin,new_basename_img)

			shutil.copy(old_path_before,new_path_before)
			idx+=1


	def rename_inner_sr(self,asin):

		out_path_asin = os.path.join(self.outdir,'V'+str(self.version),'sr',asin)
		in_path_asin =  os.path.join(self.indir,'V'+str(self.version),'sr',asin)

		RenameAmazonImgs.create_dirs(out_path_asin)

		old_basename_imgs_sr=sorted(os.listdir(in_path_asin), key=lambda x: int(x[-5]))	#Sort the named images by the last caracter.

		self.nb_imgs_sr=len(old_basename_imgs_sr)
		idx=self.idx

		for old_basename_img in old_basename_imgs_sr:

			new_basename_img='_'.join(['V'+str(self.version),asin,'3sr','IMG'+str(idx).zfill(4)])+'.jpg'

			old_path_before=os.path.join(in_path_asin,old_basename_img)
			new_path_before=os.path.join(out_path_asin,new_basename_img)

			shutil.copy(old_path_before,new_path_before)
			idx+=1
			
	def get_nb_imgs(self): 
		return self.nb_imgs_before

	def rename_all(self):

		
		self.idx = 0

		self.nb_imgs_before=0
		self.nb_imgs_after = 0 
		self.nb_imgs_sr = 0 
		
		for asin in self.list_asin:

			self.rename_inner_before(asin)
			self.rename_inner_after(asin)
			self.rename_inner_sr(asin)
			try : 
				# Update the current value of idx. 
				assert self.nb_imgs_before == self.nb_imgs_after == self.nb_imgs_sr
			except AssertionError as e: 
				print(f'Number of images in each folder: {self.nb_imgs_before,self.nb_imgs_after,self.nb_imgs_sr}')

			self.idx+=self.get_nb_imgs()



if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("--input_root_path",'-i',type=str,default='/Users/Gaetan/Desktop/amazon_imgs')
	parser.add_argument('--output_root_path','-o',type=str,default='/Users/Gaetan/Desktop/amazon_imgs_out')
	parser.add_argument("--version",'-v',type=int,default=1)

	args = parser.parse_args()

	test=RenameAmazonImgs(args.input_root_path,args.output_root_path,args.version)

