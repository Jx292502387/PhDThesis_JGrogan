#	Copyright (c) 2015 James A. Grogan
#
#       Permission is hereby granted, free of charge, to any person obtaining a copy
#       of this software and associated documentation files (the "Software"), to deal
#       in the Software without restriction, including without limitation the rights
#       to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#       copies of the Software, and to permit persons to whom the Software is
#       furnished to do so, subject to the following conditions:
#
#       The above copyright notice and this permission notice shall be included in
#       call copies or substantial portions of the Software.
#
#       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#       IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#       FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#       AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#       LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#       OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#       THE SOFTWARE.
#
#       Author: J. Grogan
#       Initial Version: 2012

# Import Neccesary Abaqus Modules
from abaqusConstants import *
from abaqus import *
# Define Part
aModel=mdb.models['Straight']
aAss=aModel.rootAssembly
bPart=aModel.parts['p3']
tb=0.24
A=2.4
ecen=0.
ellip=0.
bean_m=0.
bean_exp=1.5
t1=5.
t2=5.
xp1=0.5
xp2=0.5
rL1=11.
rL2=10.1787602
radius=rL2/(2.*pi)
r2=15.
# Map Part
nodelist=[]
coordlist=[]
for eachnode in bPart.nodes:
	x_cor=eachnode.coordinates[0]
	y_cor=eachnode.coordinates[1]
	z_cor=eachnode.coordinates[2]
	rFraction=z_cor/tb
	rindex1=(y_cor/rL1)**(-log(2.)/log(xp1))
	rbracket1=(sin(pi*rindex1))**t1
	rad_plaque=1.+A*rbracket1       
	rheight1=tb+(A-tb)*rbracket1
	theta=x_cor/radius
	x_cor=(radius-rad_plaque*z_cor)*cos(theta)
	y_cor=y_cor
	z_cor=(radius-rad_plaque*z_cor)*sin(theta)-ecen*rbracket1*rFraction
	if x_cor>0.:
		x_cor=x_cor+ellip*abs(x_cor)*rFraction*rbracket1
	else:
		x_cor=x_cor-ellip*abs(x_cor)*rFraction*rbracket1
	z_cor=z_cor+bean_m*(abs(x_cor)**bean_exp)*rFraction*rbracket1
#	theta=y_cor/r2
#    y_cor=(r2-z_cor)*cos(theta)
#    z_cor=(r2-z_cor)*sin(theta) 
	nodelist.append(eachnode)
	coordlist.append((x_cor,y_cor,z_cor))
bPart.editNode(nodes=nodelist,coordinates=coordlist)
