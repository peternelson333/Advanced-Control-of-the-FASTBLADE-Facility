import tkinter as tk
import pandas as pd
import numpy as np
import scipy, datetime, math
from tkinter import filedialog
from scipy import integrate

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import  NavigationToolbar2Tk, FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

Height=650
Width=1400

bg='gray'
otherbg='#80c1ff'


# MAIN
def run(number_rams,nodes,bounds,fname,iterations):

	if number_rams=='' or nodes=='' or bounds=='' or fname=='':	
		label['text'] = 'Not Fully Specified'

	else:
		
		if iterations=='':
			iterations=1000

		og_frame.destroy()

		lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
		lower_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.67, anchor='n')

		label = tk.Label(lower_frame)
		label.place(relwidth=1, relheight=1)

		label['text']='Loading...'

		bounds=bounds.replace('(','')
		bounds=bounds.replace(')','')
		bounds=[float(s) for s in bounds.split(',')]

		data=pd.read_excel(fname)
		number_rams=int(number_rams)
		nodes=int(nodes)
		iterations=int(iterations)
		lower_b=bounds[0]
		upper_b=bounds[1]
		L=data['radial position'][len(data)-1]

		global x

		x=list(range(0,nodes))
		b=L/(nodes-1)
		x[:]= [__ * b for __ in x]

		Fx = np.interp(x,data['radial position'],data['Fx'])              #assume both inputs are positive and names
		Fy = np.interp(x,data['radial position'],data['Fy']) 


		##################################################################################
		def targets(load):
		 	integralpart = scipy.integrate.cumtrapz(load, x)
		 	integralpart = np.insert(integralpart,0,0)
		 	TF = integralpart[-1]

		 	TargetShear = [0]*len(load) # this is an issueeeeeeeeeeeeee
		 	TargetShear[0] = TF

		 	for k in range(1,len(integralpart)):
		 		TargetShear[k] = TF-integralpart[k]
		 		integralPart=scipy.integrate.cumtrapz(TargetShear,x)
		 		integralPart = np.insert(integralPart,0,0)
		 		bmax = integralPart[-1]

		 		TargetBending = [0]*len(load) # same issue is asusmed hereeeeeeeeee
		 		TargetBending[0] = -bmax

		 	for k in range(1,len(integralPart)):
		 		TargetBending[k] = integralPart[k]-bmax

		 	return TargetShear,TargetBending, TF, bmax
		###################################################################################
		def angledF(avec):
		 	Fx=[0]*len(avec)
		 	Fy=[0]*len(avec)

		 	for i in range(0,len(avec)):
		 		Fx[i]=Fvec[i]*math.sin(math.radians(avec[i]))
		 		Fy[i]=Fvec[i]*math.cos(math.radians(avec[i]))

		 	return Fx,Fy
		##################################################################################
		def AcSh2D(longsol):
			mid=int(number_rams)
			avec=longsol[0:mid]
			lvec=longsol[mid:mid*2]

			Fx,Fy=angledF(avec)

			actualShearx=[TFx]*len(x)
			actualSheary=[TFy]*len(x)

			for i in range(0,len(x)):
				for j in range(0,len(lvec)):
					if x[i]>lvec[j]:
						actualShearx[i]=actualShearx[i]-Fx[j]
						actualSheary[i]=actualSheary[i]-Fy[j]

			return actualSheary, actualShearx
		#################################################################################
		def obj(longsol):

			if len(longsol) != number_rams*2:
				print('wrong number of rams')
			
			else:
				lsq_l=[0]*(len(x))
				actualSheary,actualShearx=AcSh2D(longsol)
				for i in range(0,len(x)):
					lsq_l[i]=abs(actualSheary[i]-TargetSheary[i]) + abs(actualShearx[i]-TargetShearx[i])

			return sum(lsq_l)
		###############################################################################
		def AcBe(AcShy, AcShx):
			integralParty=scipy.integrate.cumtrapz(AcShy,x)
			integralParty = np.insert(integralParty,0,0)
			bmaxy = integralParty[-1]
			   
			actualBendingy = [None]*len(Fx)
			actualBendingy[0] = -bmaxy

			for k in range(1,len(integralParty)):
			   actualBendingy[k] = integralParty[k]-bmaxy
			       
			integralPartx = scipy.integrate.cumtrapz(AcShx,x)
			integralPartx = np.insert(integralPartx,0,0)
			bmaxy = integralPartx[-1]
			   
			actualBendingx = [None]*len(Fx)
			actualBendingx[0] = -bmaxx

			for k in range(1,len(integralPartx)):
			   actualBendingx[k] = integralPartx[k]-bmaxx
			       
			   
			return(actualBendingy,actualBendingx)
		############################################################################
		global TargetShearx, TargetSheary, TargetBendingx, TargetBendingy

		TargetShearx,TargetBendingx,TFx,bmaxx=targets(Fx)
		TargetSheary,TargetBendingy,TFy,bmaxy=targets(Fy)

		F=TFx/number_rams
		Fvec=[F]*number_rams

		bounds=[(0,90)]*number_rams+[(lower_b*L,upper_b*L)]*number_rams

		solfinal=scipy.optimize.dual_annealing(obj,bounds,maxiter=iterations)

		n=np.sort(solfinal.x)

		global angles, positions, ActualShearx, ActualSheary, ActualBendingx, ActualBendingy

		angles=n[0:int(number_rams)]
		positions=n[int(number_rams):int(number_rams)*2]

		ActualSheary, ActualShearx = AcSh2D(n)
		ActualBendingy,ActualBendingx=AcBe(ActualSheary,ActualShearx)

		f, (ax1, ax2) = plt.subplots(1, 2)

		ax1.step(x,ActualShearx,'b', label='Actual Shear Force (x)',lw=0.9, where='post')
		ax1.plot(x,TargetShearx,'r', label = 'Target Shear Force (x)',ls='--')
		ax1.step(x,ActualSheary,'g', label='Actual Shear Force (y)',lw=0.9, where='post')
		ax1.plot(x,TargetSheary,'black', label = 'Target Shear Force (y)',ls='--')
		ax1.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
		ax1.set_xlabel('Blade Specimen (mm)')
		ax1.set_ylabel('Shear Force (N)')
		ax1.set_title('Shear Force Diagram')
		ax1.legend(loc='best')

		ax2.plot(x,ActualBendingx,'b', label='Actual Bending Moment (x)',lw=0.9)
		ax2.plot(x,TargetBendingx,'r', label = 'Target Bending Moment (x)',ls='--')
		ax2.plot(x,ActualBendingy,'g', label='Actual Bending Moment (y)',lw=0.9)
		ax2.plot(x,TargetBendingy,'black', label = 'Target Bending Moment (y)',ls='--')
		ax2.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
		ax2.set_xlabel('Blade Specimen (mm)')
		ax2.set_ylabel('Bending Moment (Nm)')
		ax2.set_title('Bending Moment Diagram')
		ax2.legend(loc='best')

		plt.tight_layout()
		
		canvas=FigureCanvasTkAgg(f,lower_frame)
		toolbar=NavigationToolbar2Tk(canvas, lower_frame)
		canvas._tkcanvas.place(relx=0.05,rely=0, relwidth=0.9,relheight=0.93)



def export():
	d = {'Nodes':x,'TargetShearx':TargetShearx,'ActualShearx':ActualShearx, 'TargetSheary': TargetSheary,'ActualSheary':ActualSheary, 'TargetBendingx':TargetBendingx,'ActualBendingx':ActualBendingx, 'TargetBendingy':TargetBendingy,'ActualBendingy':ActualBendingy}
	df = pd.DataFrame(data=d)

	d2={'Angles': angles, 'Positions':positions}
	df2=pd.DataFrame(data=d2)

	writer = pd.ExcelWriter('Results.xlsx')

	df2.to_excel(writer,sheet_name='Solution',index=False)
	df.to_excel(writer, sheet_name='Output',index=False)
	writer.save()
	writer.close()



def browse_file():
	fname = filedialog.askopenfilename(filetypes = (("Excel XLSX Files", "*.xlsx"), ("All files", "*")))
	filepaththing['text'] = fname


# INITIALISING

root= tk.Tk()
root.title("Rams Calculator")
canvas=tk.Canvas(root,height=Height, width=Width)
canvas.pack()

background_image=tk.PhotoImage(file='Fb.png')
background_label=tk.Label(root,image=background_image)
background_label.place(relwidth=1,relheight=1)

frame= tk.Frame(root,bg=bg)
frame.place(relx=0.02,rely=0.02, relwidth=0.96,relheight=0.96)

root.iconbitmap('Fb.ico')


# TITLE

label=tk.Label(frame,text="FASTBLADE Rams Calculator- Peter Nelson", bg='#80c1ff', font=40)
label.place(relx=0.32,rely=0,relwidth=0.35,relheight=0.05)


# INPUT LABELS 

h_in1=0.1


namesize=12

#Path
label_filepath=tk.Label(frame,text="File Path:", bg=bg)
label_filepath.place(relx=0.06,rely=h_in1,relwidth=0.1,relheight=0.05)
label_filepath.config(font=("Arial", namesize))

filepath = tk.Button(frame, text = 'Browse', bg='orange', fg='black', width = 6, command=browse_file)
filepath.place(relx=0.15,rely=h_in1,relwidth=0.05,relheight=0.05)

#Nodes
label_nodes=tk.Label(frame,text="Nodes:", bg=bg)
label_nodes.place(relx=0.23,rely=h_in1,relwidth=0.07,relheight=0.05)
label_nodes.config(font=("Arial", namesize))

nodes=tk.Entry(frame,bg='red')
nodes.place(relx=0.29,rely=h_in1,relwidth=0.04,relheight=0.05)

#Bounds
label_bounds=tk.Label(frame,text="Bounds:", bg=bg)
label_bounds.place(relx=0.35,rely=h_in1,relwidth=0.1,relheight=0.05)
label_bounds.config(font=("Arial", namesize))

bounds=tk.Entry(frame,bg='red')
bounds.place(relx=0.43,rely=h_in1,relwidth=0.04,relheight=0.05)

#Number_rams
label_nr=tk.Label(frame,text="Ram Number:", bg=bg)
label_nr.place(relx=0.51,rely=h_in1,relwidth=0.08,relheight=0.05)
label_nr.config(font=("Arial", namesize))

number_rams=tk.Entry(frame,bg='red')
number_rams.place(relx=0.6,rely=h_in1,relwidth=0.04,relheight=0.05)


#Iterations
label_it=tk.Label(frame,text="Iterations:", bg=bg)
label_it.place(relx=0.66,rely=h_in1,relwidth=0.09,relheight=0.05)
label_it.config(font=("Arial", namesize))

itera=tk.Entry(frame,bg='red')
itera.place(relx=0.74,rely=h_in1,relwidth=0.04,relheight=0.05)


# INVISIBLE FILEPATH LABEL
filepaththing=tk.Label(frame,bg=bg,fg=bg)
filepaththing.place(relx=0.,rely=0,relwidth=0.01,relheight=0.01)



# RUN BUTTON

button=tk.Button(frame, text="Run", bg='green',fg='white', command=lambda: run(number_rams.get(),nodes.get(),bounds.get(),filepaththing['text'],itera.get()))
button.place(relx=0.83,rely=h_in1, relwidth=0.06,relheight=0.06)


# EXPORT BUTTON

button=tk.Button(frame, text="Export", bg='green',fg='white', command=lambda: export())
button.place(relx=0.46,rely=0.92, relwidth=0.08,relheight=0.06)



# Original Frame
og_frame = tk.Frame(root, bg='#80c1ff', bd=10)
og_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.67, anchor='n')

label = tk.Label(og_frame)
label.place(relwidth=1, relheight=1)


root.mainloop()