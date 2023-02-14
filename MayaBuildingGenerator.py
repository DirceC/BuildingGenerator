#Maya tool to generate simple buildings based on user input
#Diferent tabs to duplicate objects and place them over a plane and to create basic lighting
import maya.cmds as cmds
import random

#Global variables
ComponentType=0
lightPosVar=1
UIwidthVar=550
nameVar=0



#Create window 
def MakeUI():
    
    if cmds.window("WinBuild",exists=True):
        cmds.deleteUI("WinBuild")

    #Window master layout
    UIwindow=cmds.window("WinBuild",t="Environment generator",w=UIwidthVar,h=250,s=True)
    cmds.formLayout(nd=100)
    #Tabs layout
    tabs=cmds.tabLayout(bs="full",w=UIwidthVar)
    #First tab
    fTab=cmds.columnLayout(cal="center",adj=True)
    cmds.tabLayout(tabs,edit=True,tl=[fTab,"Populate"])
    #Populate frame layout
    cmds.frameLayout(l="Populate",bgc=(0.2, 0.2, 0.2), bgs=True, en=True, mw=4, mh=4)
    #Form layout
    buildForm=cmds.formLayout(nd=100)
    buildTx=cmds.text("Select same type of objects to populate along a curve",al="center")
    #Row column for buttons
    buildRCL=cmds.rowColumnLayout(nc=2,cw=[(1,150),(2,150)],co=[(1,"right",4),(2,"left",4)])
    buildBtnAdd=cmds.button(l="Add",w=100,c="addSelection()")
    MakeUI.buildBtnRmv=cmds.button(l="Remove",w=100,c="RemSelection()",en=False)
    cmds.setParent("..")
    #List of added objects for buildings
    MakeUI.buildObjList=cmds.textScrollList(sc="makeSelection()",ams=True)
    #Form layout order
    cmds.formLayout(buildForm,edit=True,af=[(buildTx,'top',2),(buildTx,'left',2),(buildTx,'right',2),(buildRCL,'top',20),(buildRCL,'left',115),(buildRCL,'right',2),(MakeUI.buildObjList,'left',100),(MakeUI.buildObjList,'right',100)],ac=[(MakeUI.buildObjList,'top',5,buildRCL)])
    cmds.setParent("..")
    #Row column for type of objects selection
    cmds.rowColumnLayout(nc=4,cw=[(1,100),(2,100),(3,100),(4,100)])
    #Radio Button selection of type of objects
    cmds.text("Type of objects:")
    cmds.radioCollection()
    cmds.radioButton(l="Buildings",cc="ComponentType=0",sl=True)
    cmds.radioButton(l="Trees",cc="ComponentType=1")
    cmds.radioButton(l="Rocks",cc="ComponentType=2")
    cmds.setParent("..")
    #Curve selection
    MakeUI.selectedCurve=cmds.textFieldButtonGrp(l="Select the Curve:",ed=False,bl="Select",bc="SelectCRV()")
    #Naming for the objects
    MakeUI.OBJname=cmds.textFieldGrp(l="Name for objects:")
    cmds.text("Highlight all the objects in the list that are going to be used")
    #Object class creation
    MakeUI.selectionBtn=cmds.button(l="Complete selection",c="Creation()",en=False)
    MakeUI.changeSelectionBtn=cmds.button(l="Change selection",c="ChangeSel()",en=False)
    cmds.separator()
    #Populate user variables 
    MakeUI.NumofCopies=cmds.intSliderGrp(l="number of copies:",v=10,f=True,min=2,max=100)
    MakeUI.OfXV=cmds.floatSliderGrp(l="X Offset",v=0,f=True,min=0)
    MakeUI.OfYV=cmds.floatSliderGrp(l="Y Offset",v=0,f=True,min=0)
    MakeUI.OfZV=cmds.floatSliderGrp(l="Z Offset",v=0,f=True,min=0)
    MakeUI.ScaleRndMin=cmds.floatSliderGrp(l="Scale min",v=1,f=True,min=0.1,max=10)
    MakeUI.ScaleRndMax=cmds.floatSliderGrp(l="Scale max",v=1,f=True,min=0.1,max=10)
    MakeUI.populateBtn=cmds.button(l="Populate",c="Populate()",en=False)
    #Row column layout for undo and finalize buttons
    cmds.rowColumnLayout(nc=2,cw=[(1,260),(2,200)],co=[(1,"right",4),(2,"left",4)])
    MakeUI.undoBtn=cmds.button(l="Undo",c="UndoFunc()",w=100,en=False)
    MakeUI.finalizeBtn=cmds.button(l="Finalize",c="FinalizeFun()",w=100,en=False)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    #Second tab
    sTab=cmds.columnLayout()
    #Lighting tab
    cmds.tabLayout(tabs,edit=True,tl=[sTab,"Lighting"])
    cmds.formLayout(nd=100)
    #Sunlight frame layout
    cmds.frameLayout(l="Sunlight",bgc=(0.2, 0.2, 0.2), bgs=True, en=True, mw=4, mh=4, w=UIwidthVar)
    cmds.text("Create a directional light that will be moved to the desired position")
    #Get the user name for the light
    MakeUI.lightName=cmds.textFieldButtonGrp(l="Name the light:", tx="directionalLight", bl="Enter", cw3=[100,230,100])
    #Row column for radio button
    cmds.rowColumnLayout(nc=4,cw=[(1,100),(2,100),(3,100),(4,100)])
    #Axis for the position of the "sunlight"
    cmds.text("Select Axis:")
    cmds.radioCollection()
    cmds.radioButton(l="X",cc="lightPosVar=0")
    cmds.radioButton(l="Y",cc="lightPosVar=1",sl=True)
    cmds.radioButton(l="Z",cc="lightPosVar=2")
    cmds.setParent("..")
    #row column for create and delete buttons
    cmds.rowColumnLayout(nc=2,cw=[(1,220),(2,210)],co=[(1,"right",4),(2,"left",4)])
    MakeUI.createLightBtn = cmds.button(l="Create light",c="CreateLight()",w=100, en=True)
    MakeUI.deleteLightBtn = cmds.button(l="Delete",c="DeleteLight()", w=100, en=False)
    cmds.setParent("..")
    #Change light position and intensity
    MakeUI.lightPosition=cmds.intSliderGrp(l="Change position in degrees:",f=True,min=0,max=180,v=0,cc="LightPosition()", cw3=[150,100,50])
    MakeUI.lightInt=cmds.intSliderGrp(l="Change intensity:",f=True,min=0,max=100,v=1,fmx=10000,cc="LightIntensity()", cw3=[150,100,50]) 
    #Finalize light button
    MakeUI.finalizeLightBtn = cmds.button(l="Finalize",c="FinalizeLight()", en=False)   
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    
    
    #Third tab
    tTab=cmds.columnLayout()
    #Create road/river tab
    cmds.tabLayout(tabs,edit=True,tl=[tTab,"Road/River"])
    cmds.formLayout(nd=100)
    #Frame layout for road/river creation
    cmds.frameLayout(l="Road and river",bgc=(0.2, 0.2, 0.2), bgs=True, en=True, mw=4, mh=4, w=UIwidthVar)    
    cmds.text(l="Making road or river")
    #Get modifying values from user
    MakeUI.RRWidth=cmds.floatSliderGrp(l="Width",v=1,f=True,min=0.1,max=10,cc="RoadWD=cmds.floatSliderGrp(MakeUI.RRWidth,q=True,v=True)")
    MakeUI.RRDiv=cmds.intSliderGrp(l="Division",v=1,f=True,min=0.1,max=100,cc="RoadDV=cmds.intSliderGrp(MakeUI.RRDiv,q=True,v=True)")
    MakeUI.RoadRivOffset=cmds.floatSliderGrp(l="Height Offset",v=0,f=True,min=0,max=10,cc="RoadOffset=cmds.floatSliderGrp(MakeUI.RoadRivOffset,q=True,v=True)")
    #Curve selection
    MakeUI.selectedCurve2=cmds.textFieldButtonGrp(l="Select the Curve:",ed=False,bl="Select",bc="SelectCRV2()")
    #Get name for road/river
    MakeUI.rrName=cmds.textFieldButtonGrp(l="Name:",bl="Select",bc="nameVar=cmds.textFieldButtonGrp(MakeUI.rrName,q=True,tx=True)")
    #Row column for river checkbox
    cmds.rowColumnLayout(nc=1,cw=[(1,400)],co=[(1,"both",110)])
    MakeUI.RiverCheck=cmds.checkBox(l="River Only",v=False)
    cmds.setParent("..")
    #Row column for make/reset buttons
    cmds.rowColumnLayout(nc=2,cw=[(1,260),(2,200)],co=[(1,"right",4),(2,"left",4)])
    MakeUI.MakeBtn=cmds.button(l="Make Road/River",c="MakeRoadRiver()",en=True)
    MakeUI.ResetBtn=cmds.button(l="Reset Road/River",c="ResetRoadRiver()",en=False)
    cmds.setParent("..")
    #Shading option buttons
    cmds.rowColumnLayout(nc=2,cw=[(1,260),(2,200)],co=[(1,"right",4),(2,"left",4)])
    MakeUI.ShadeBtn=cmds.button(l="Shade road",c="roadShader()",en=False)
    MakeUI.ShadeRiverBtn=cmds.button(l="Shade river",c="riverShader()",en=False)
    cmds.setParent("..")
    #Finalize road/river button
    MakeUI.EndrrBtn=cmds.button(l="Finalize",c="endRivRoad()",en=False)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
   
   
    #THIS PART IS FROM MY CAPSTONE
    #Fourth tab
    frTab=cmds.columnLayout() 
    #Building creation tab   
    cmds.tabLayout(tabs,edit=True,tl=[frTab,"Building"])
    cmds.formLayout(nd=100)
    cmds.columnLayout(adj=True)
    #FRAME LAYOUT for the window section
    MakeUI.planeFL=cmds.frameLayout(l="Windows",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=False, en=True, mw=4, mh=4, w=550)
    MakeUI.FL1=cmds.formLayout(nd=100)
    MakeUI.text1=cmds.text("Create a window on the provided plane")
    MakeUI.text2=cmds.text("If you already have one make sure is parented under the 'Window' group")
    MakeUI.text3=cmds.text("If you don't have a group, select your object before pressing the button and one will be created")
    #Creating a plane for the window or skiping if one already exists
    MakeUI.createPlaneBtn=cmds.button(l="Create plane",c="WindowPlane()",w=100,en=True)
    MakeUI.alreadyPlaneBtn=cmds.button(l="Already have one",w=100,c="ExistingPlane()",en=True)
    cmds.formLayout(MakeUI.FL1, e=True, af=[(MakeUI.text1,'top',5),(MakeUI.text1,'left',165),(MakeUI.text2,'top',20),(MakeUI.text2,'left',80),(MakeUI.text3,'top',35),(MakeUI.text3,'left',20),(MakeUI.createPlaneBtn,'top',60),(MakeUI.createPlaneBtn,'left',165),(MakeUI.alreadyPlaneBtn,'top',60)], ac=[(MakeUI.alreadyPlaneBtn,'left',5,MakeUI.createPlaneBtn)])    
    cmds.setParent("..")
    #FRAME LAYOUT for creating a new plane for the window
    MakeUI.planeAttrFL=cmds.frameLayout(l="Plane",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4)
    cmds.separator(nbg=True,st="none")
    cmds.text("Modify the size of the plane,")
    cmds.text("this size will be used for all sections (doors, walls)")
    cmds.separator(h=2,nbg=True,st="none")
    #Get size and subdivisions of the section from user
    MakeUI.sectionWidth=cmds.intSliderGrp(l="Width",f=True,v=10,min=10, max=100, fmn=1, fmx=1000,cw3=[105,80,200],cc="SectionsWidth()",vis=True)
    MakeUI.sectionHeight=cmds.intSliderGrp(l="Height",f=True,v=10,min=10, max=100, fmn=1, fmx=1000,cw3=[105,80,200],cc="SectionsHeight()",vis=True)
    cmds.separator(h=4,st="in")
    MakeUI.sectionSDx=cmds.intSliderGrp(l="Subdivisions width",f=True,v=3,min=1, max=10, fmn=1, fmx=1000,cw3=[105,80,200],cc="WindowPlaneSubDivX()",vis=True)
    MakeUI.sectionSDy=cmds.intSliderGrp(l="Subdivisions heigth",f=True,v=3,min=1, max=10, fmn=1, fmx=1000,cw3=[105,80,200],cc="WindowPlaneSubDivY()",vis=True)
    MakeUI.confirmPlaneBtn=cmds.button(l="Confirm attributes",c="ConfirmAttr()",en=False)
    #User modifies the plane to make a window
    cmds.text("Make your window on the plane before proceding")
    cmds.text("Make sure your geometry is under the 'Window' group")
    cmds.text("or select the geometry before proceding and the group will be created for you")
    #Proceed if window is ready or go back
    MakeUI.makePlaneBtn=cmds.button(l="Done",c="WindowPlaneEnd()",en=False)
    cmds.button(l="Go back",c="DeletePlane()")
    cmds.setParent("..")
    #FRAME LAYOUT for existing window plane
    MakeUI.planeSizeFL=cmds.frameLayout(l="Existing Plane",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4)
    cmds.separator(nbg=True,st="none")
    #Ask the user to place locators to get the planes width and height
    cmds.text("The dimensions of the plane are needed")
    cmds.text("Four locators will be created, attach each one to the corners of your plane")
    cmds.text("Make sure the plane is facing the Z axis")
    cmds.rowColumnLayout(nc=2,cw=[(1,270),(2,200)],co=[(1,"right",5),(2,"left",5)])
    MakeUI.locBtn=cmds.button(l="Create locators", c="Locators()",w=100)
    MakeUI.deleteLocBtn=cmds.button(l="Delete locators", c="DeleteLoc()",en=False,w=100)
    cmds.setParent("..")
    cmds.rowColumnLayout(nc=2,cw=[(1,270),(2,200)],co=[(1,"right",5),(2,"left",5)])
    MakeUI.goBackBtn=cmds.button(l="Go back", c="GoBack()",w=100)
    #Confirm dimensions of the window plane
    MakeUI.locConfirm=cmds.button(l="Confirm", c="GetDimensions()",en=False,w=100)
    cmds.setParent("..")
    cmds.setParent("..")
    #END OF FRAME LAYOUT for window
    cmds.setParent("..")
    #FRAME LAYOUT for creating a door
    MakeUI.doorFL=cmds.frameLayout(l="Door",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4, w=550)
    MakeUI.FL2=cmds.formLayout(nd=100)
    #Create a plane for the user to make a door or skip if one laready exists
    MakeUI.text4=cmds.text("Create a door on the provided plane")
    MakeUI.text5=cmds.text("If you already have one make sure is parented under the 'Door' group")
    MakeUI.text6=cmds.text("If you don't have a group, select your object before pressing the button and one will be created")
    MakeUI.text7=cmds.text("Your plane has to be the same size as the previous, adjust the corners if necessary")
    MakeUI.createDoorBtn=cmds.button(l="Create plane",c="DoorPlane()",w=100,en=True)
    MakeUI.alreadyDoorBtn=cmds.button(l="Already have one",w=100,c="ExistingDoor()",en=True)
    MakeUI.doorGoBackBtn=cmds.button(l="Go back", c="DoorGoBack()",w=100)
    cmds.formLayout(MakeUI.FL2, e=True, af=[(MakeUI.text4,'top',5),(MakeUI.text4,'left',165),(MakeUI.text5,'top',20),(MakeUI.text5,'left',80),(MakeUI.text6,'top',35),(MakeUI.text6,'left',20),(MakeUI.text7,'top',50),(MakeUI.text7,'left',55),(MakeUI.createDoorBtn,'top',75),(MakeUI.createDoorBtn,'left',165),(MakeUI.alreadyDoorBtn,'top',75),(MakeUI.doorGoBackBtn,'top',105),(MakeUI.doorGoBackBtn,'left',220)], ac=[(MakeUI.alreadyDoorBtn,'left',5,MakeUI.createDoorBtn)])    
    cmds.setParent("..")
    #FRAME LAYOUT for creating a new plane for the door
    MakeUI.planeDoorFL=cmds.frameLayout(l="Plane",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4)
    cmds.text("Create a door on the given plane")
    cmds.text("Make sure your geometry is under the 'Door' group")
    cmds.text("or select the geometry before proceding and the group will be created for you")
    cmds.button(l="Done",c="DoorConfirm()")
    cmds.button(l="Go back",c="DoorGoBack2()")
    cmds.setParent("..")
    cmds.setParent("..")
    #FRAME LAYOUT for creating the size of the building
    MakeUI.buildingFL=cmds.frameLayout(l="Building",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4)  
    MakeUI.GoBackMod=cmds.button(l="Go Back",c="GoBackMod()",en=True)
    cmds.separator(h=2,nbg=True,st="none")
    #Get width, depth and height of the building from the user
    cmds.text("Width and depth of building in # of panels")
    cmds.separator(h=1,nbg=True,st="none")
    MakeUI.buildingWidth=cmds.intSliderGrp(l="Width",f=True,v=1,min=1, max=100, fmn=1, fmx=1000,cw3=[105,80,200],cc="BuildingWidth()",en=True)
    MakeUI.buildingDepth=cmds.intSliderGrp(l="Depth",f=True,v=1,min=1, max=100, fmn=1, fmx=1000,cw3=[105,80,200],cc="BuildingDepth()",en=True)
    MakeUI.ConfirmWD=cmds.button(l="Confirm",c="ConfirmWD()")
    MakeUI.buildingHeight=cmds.intSliderGrp(l="Height",f=True,v=1,min=1, max=100, fmn=1, fmx=1000,cw3=[105,80,200],cc="BuildingHeight()",en=False)
    cmds.rowColumnLayout(nc=2,cw=[(1,270),(2,200)],co=[(1,"right",5),(2,"left",5)])
    MakeUI.GoBackHeight=cmds.button(l="Go Back",c="GoBackHeight()",en=False,w=100)
    #Confirm dimensions and make the building
    MakeUI.MakeBuilding=cmds.button(l="Make Building",c="ConfirmBuild()",en=False,w=100)
    cmds.setParent("..")
    cmds.setParent("..")
    #FRAME LAYOUT to finalize the building 
    MakeUI.finalize=cmds.frameLayout(l="Finalize",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4) 
    #FRAME LAYOUT for placing the windows on the building
    MakeUI.finalizeWin=cmds.frameLayout(l="Windows",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=False, en=True, mw=4, mh=4)
    MakeUI.GoBackBuilding=cmds.button(l="Go Back",c="GoBackBuild()",en=True)
    #Ask the user to select planes where they want the windows
    cmds.text(l="Select all the planes where you want to place windows")
    cmds.rowColumnLayout(nc=2,cw=[(1,270),(2,200)],co=[(1,"right",5),(2,"left",5)])
    MakeUI.addWindows=cmds.button(l="Add",c="addSelectionW()",w=100)
    MakeUI.remWindows=cmds.button(l="Remove",c="RemSelectionW()",w=100)
    cmds.setParent("..")
    cmds.rowColumnLayout(nc=3,cw=[(1,120),(2,300),(3,100)])
    cmds.separator(nbg=True,st="none")
    MakeUI.SLObjList=cmds.textScrollList(ams=True,sc="SelectPlanes()")  
    cmds.separator(nbg=True,st="none")
    cmds.setParent("..")
    #Place the windows
    MakeUI.makeWindows=cmds.button(l="Place",c="PlaceWindows()")
    cmds.separator(nbg=True,st="none")
    cmds.setParent("..")
    #FRAME LAYOUT for placing doors on the building
    MakeUI.finalizeDoor=cmds.frameLayout(l="Doors",bgc=(0.2, 0.2, 0.2), bgs=True, cll=True, cl=True, en=False, mw=4, mh=4)
    #Ask the user to select planes where they want the doors
    MakeUI.backWindows=cmds.button(l="Go Back",c="GoBackWindows()",en=False)
    cmds.text(l="Select all the planes where you want to put doors")
    cmds.rowColumnLayout(nc=2,cw=[(1,270),(2,200)],co=[(1,"right",5),(2,"left",5)])
    MakeUI.addDoor=cmds.button(l="Add",c="addSelectionD()",w=100)
    MakeUI.remDoor=cmds.button(l="Remove",c="RemSelectionD()",w=100)
    cmds.setParent("..")
    cmds.rowColumnLayout(nc=3,cw=[(1,120),(2,300),(3,100)])
    cmds.separator(nbg=True,st="none")
    MakeUI.SLObjListD=cmds.textScrollList(ams=True,sc="SelectPlanesDoor()")  
    cmds.separator(nbg=True,st="none")
    cmds.setParent("..")
    #Place the doors
    MakeUI.makeDoor=cmds.button(l="Place",c="PlaceDoor()")
    MakeUI.backDoor=cmds.button(l="Go Back",c="GoBackDoor()",en=False)
    cmds.separator(nbg=True,st="none")
    #Delete extra planes, create a roof and group everything together to finish the building
    MakeUI.finishBuilding=cmds.button(l="Finalize Building",c="FinishBuilding()",en=False)
    cmds.separator(nbg=True,st="none")
    cmds.setParent("..")
    cmds.setParent("..")


    #Window master layout end
    cmds.setParent("..")
    cmds.showWindow()

MakeUI()

#----------Classes----------

#Selected objects class
class selectedItems(object):
    def __init__(self,name,selItem):
        self.name=name
        self.selItem=selectedItem
    #Multiply objects function
    def MultiplyObj(self,DupNum,RndMinScale,RndMaxScale,OffXVal,OffYVal,OffZVal):
        #Set the starting position for the multiplied objects
        cmds.spaceLocator(n="MainLoc")
        cmds.select(SelectCRV.selectedCV[0],add=True)   
        #Motion path with lenght of the copies     
        cmds.pathAnimation(fm=True,f=True,fa="x",ua="y",inverseFront=False,stu=0,etu=DupNum)
        cmds.selectKey("motionPath1_uValue")
        cmds.keyTangent(itt="linear",ott="linear")    
        #Create parent grouo for copies
        ParentGroup=cmds.group(em=True,n="Blocks")
        #Multiply loop
        for obj in range(0,DupNum):
            lenght=len(self.selItem)
            i=int(random.uniform(0,lenght))
            #Random number for scale
            RandomScaling=random.uniform(RndMinScale,RndMaxScale)
            cmds.currentTime(obj,e=True)
            #Get current position
            CurX=cmds.getAttr("MainLoc.tx")
            CurY=cmds.getAttr("MainLoc.ty")
            CurZ=cmds.getAttr("MainLoc.tz")
            CurRotY=cmds.getAttr("MainLoc.ry")
            #Select and duplicate object
            cmds.select(self.selItem[i],r=True)
            tempObj=cmds.duplicate(n=self.name)
            #Move object to new position
            cmds.setAttr(tempObj[0]+".tx",CurX+OffXVal)
            cmds.setAttr(tempObj[0]+".ty",CurY+OffYVal)
            cmds.setAttr(tempObj[0]+".tz",CurZ+OffZVal)
            cmds.setAttr(tempObj[0]+".ry",CurRotY)
            #Scale object
            cmds.scale(RandomScaling,RandomScaling,RandomScaling)
            #Parent under group
            cmds.parent(tempObj[0],"Blocks",r=False)
            print(self.selItem[i])
        cmds.delete("MainLoc")
            
                

#---------Functions---------
#Create object instance for diferent types of objects
def Creation():
    #Get name from user
    Creation.Username=cmds.textFieldGrp(MakeUI.OBJname,q=True,tx=True)
    #Get type of object from radio button selection
    selection=selectedItem
    if ComponentType==0:
        Creation.Buildings = selectedItems(Creation.Username,selection)
    if ComponentType==1:
        Creation.Trees = selectedItems(Creation.Username,selection)
    if ComponentType==3:
        Creation.Rocks = selectedItems(Creation.Username,selection)
    #Change buttons status
    cmds.button(MakeUI.selectionBtn,en=False,e=True)
    cmds.button(MakeUI.changeSelectionBtn,e=True,en=True)
    cmds.button(MakeUI.populateBtn,e=True,en=True)

#Function to duplicate and place objects along the curve        
def Populate():
    #Get all the user entered data, such as offset and rand scale
    Dups=cmds.intSliderGrp(MakeUI.NumofCopies,q=True,v=True)
    OffX=cmds.floatSliderGrp(MakeUI.OfXV,q=True,v=True)
    OffY=cmds.floatSliderGrp(MakeUI.OfYV,q=True,v=True)
    OffZ=cmds.floatSliderGrp(MakeUI.OfZV,q=True,v=True)
    randMinScale=cmds.floatSliderGrp(MakeUI.ScaleRndMin,q=True,v=True)
    randMaxScale=cmds.floatSliderGrp(MakeUI.ScaleRndMax,q=True,v=True)
    #Create the objects according to the type selected by the user
    if ComponentType==0:
        Creation.Buildings.MultiplyObj(Dups,randMinScale,randMaxScale,OffX,OffY,OffZ)
    if ComponentType==1:
        Creation.Trees.MultiplyObj(Dups,randMinScale,randMaxScale,OffX,OffY,OffZ)
    if ComponentType==3:
        Creation.Rocks.MultiplyObj(Dups,randMinScale,randMaxScale,OffX,OffY,OffZ)
    #Change buttons status
    cmds.button(MakeUI.undoBtn,e=True,en=True)
    cmds.button(MakeUI.finalizeBtn,e=True,en=True)

#Function to add objects to the list    
def addSelection():
        selectedOBJs=cmds.ls(sl=True,o=True)
        for i in selectedOBJs:
            cmds.textScrollList(MakeUI.buildObjList,e=True,a=i)
            print ("the selected objs are:"+ str(selectedOBJs))
        cmds.select(cl=True)
        #Change buttons status
        cmds.button(MakeUI.buildBtnRmv,e=True,en=True)
        cmds.button(MakeUI.selectionBtn,e=True,en=True)

#Function to remove objects from the list                
def RemSelection():
        selectedItem=cmds.textScrollList(MakeUI.buildObjList,q=True,si=1)
        cmds.textScrollList(MakeUI.buildObjList,e=True,ri=selectedItem)
        
#Function to select objects from the list        
def makeSelection():
        global selectedItem
        selectedItem=cmds.textScrollList(MakeUI.buildObjList,q=True,si=1)
        print ("user selected this object: "+selectedItem[0])    
        return selectedItem 

#Function to select the curve
def SelectCRV():
        SelectCRV.selectedCV=cmds.ls(sl=True,o=True)
        print (SelectCRV.selectedCV)
        #Change buttons status
        cmds.textFieldButtonGrp(MakeUI.selectedCurve,e=True,tx=SelectCRV.selectedCV[0])    

#Function to change the selected objects
def ChangeSel():
    #Change buttons status
    cmds.button(MakeUI.selectionBtn,en=True,e=True)
    cmds.button(MakeUI.changeSelectionBtn,e=True,en=False)
    cmds.button(MakeUI.populateBtn,e=True,en=False)

#Function to undo the object duplication    
def UndoFunc():
    cmds.select("MainLoc")
    cmds.delete()
    cmds.select("Blocks")
    cmds.delete()
    #Change buttons status
    cmds.button(MakeUI.undoBtn,e=True,en=False)
    cmds.button(MakeUI.finalizeBtn,e=True,en=False)

#Function to finalize the duplication    
def FinalizeFun():
    cmds.select("MainLoc")
    cmds.delete()
    cmds.select("Blocks")
    cmds.rename("Blocks",Creation.Username)
    #Change buttons status
    cmds.button(MakeUI.undoBtn,e=True,en=False)
    cmds.button(MakeUI.finalizeBtn,e=True,en=False)
    cmds.button(MakeUI.populateBtn,e=True,en=False)
    cmds.button(MakeUI.selectionBtn,en=False,e=True)
    cmds.button(MakeUI.changeSelectionBtn,e=True,en=False)
    cmds.button(MakeUI.buildBtnRmv,e=True,en=True)

#Function to create the "sunlight"        
def CreateLight():
    #Get light name from user
    CreateLight.userLightName=cmds.textFieldButtonGrp(MakeUI.lightName,q=True, tx=True)
    #Group to modify the position of the light
    cmds.group(em=True,n="Light")   
    #Create a directional light on the user selected axis
    cmds.button(MakeUI.createLightBtn,en=False, e=True)
    if lightPosVar==0:
        cmds.directionalLight(rotation=(-90,0,0), n=CreateLight.userLightName) 
    if lightPosVar==1:
        cmds.directionalLight(rotation=(0,90,0), n=CreateLight.userLightName)      
    if lightPosVar==2:
        cmds.directionalLight(rotation=(0,90,0), n=CreateLight.userLightName)
    #Change buttons status
    cmds.select(CreateLight.userLightName)
    cmds.parent(CreateLight.userLightName,"Light",r=False)
    cmds.button(MakeUI.deleteLightBtn, e=True, en=True)
    cmds.button(MakeUI.finalizeLightBtn, e=True, en=True)

#Function to delete the light      
def DeleteLight():
    cmds.select(CreateLight.userLightName)
    cmds.delete()
    cmds.select("Light")
    cmds.delete()
    #Change buttons status
    cmds.button(MakeUI.createLightBtn,en=True, e=True)
    cmds.button(MakeUI.deleteLightBtn, e=True, en=False)
    cmds.button(MakeUI.finalizeLightBtn, e=True, en=False)

#Function to change the light position
def LightPosition():    
    #Get position from user
    lightRotation=cmds.intSliderGrp(MakeUI.lightPosition,q=True,v=True)   
    #Change position depending on axis
    if lightPosVar==0:
        cmds.select("Light")
        cmds.rotate(lightRotation,0,0)
    if lightPosVar==1:
        cmds.select("Light")
        cmds.rotate(0,-lightRotation,0)
    if lightPosVar==2:
        cmds.select("Light")
        cmds.rotate(0,0,lightRotation)

#Function to change light intensity
def LightIntensity():
    #Get values from user 
    lightUserInt=cmds.intSliderGrp(MakeUI.lightInt, q=True, v=True)
    #select light and set new intensity
    lightShape=cmds.ls(sl=True)
    cmds.setAttr(CreateLight.userLightName+".intensity", lightUserInt)

#Function to finalize the light        
def FinalizeLight():
    #Select the light group and delete it
    cmds.select("Light")
    cmds.parent(CreateLight.userLightName,"Light",w=True) 
    cmds.delete("Light")
    #Change buttons status
    cmds.button(MakeUI.createLightBtn, e=True, en=True)
    cmds.button(MakeUI.deleteLightBtn, e=True, en=False)
    cmds.button(MakeUI.finalizeLightBtn, e=True, en=False)

#Function to select the curve
def SelectCRV2():
        SelectCRV2.selectedCV=cmds.ls(sl=True,o=True)
        print (SelectCRV2.selectedCV)
        #Change buttons status
        cmds.textFieldButtonGrp(MakeUI.selectedCurve2,e=True,tx=SelectCRV2.selectedCV[0])   

#Function to make a road or a river
def MakeRoadRiver():
    #Create a plane with user provided width
    cmds.polyPlane(n="RoadRiverBase",sh=1,sw=1,w=RoadWD)
    #Attach the plane to the selected curve and extrude to the length
    cmds.select(SelectCRV2.selectedCV[0],add=True)
    cmds.pathAnimation(fm=True,f=True,fa="z",ua="y",iu=False,inverseFront=False,stu=0,etu=1)
    theRoadRiver=cmds.polyExtrudeEdge("RoadRiverBase.e[0]",inc=SelectCRV2.selectedCV[0],d=RoadDV)
    cmds.select("RoadRiverBase",r=True)
    cmds.DeleteMotionPaths()
    #Select and delete faces that don't work
    cmds.select("RoadRiverBase.f[0]")
    cmds.delete()
    cmds.select("RoadRiverBase.f[0]")
    cmds.delete()
    #Get the position of the normals
    faceNormals=cmds.polyInfo("RoadRiverBase",fn=True)
    rndFace=int(random.uniform(0,len(faceNormals)))
    #Get the normal position from a random face
    rndFaceSel=faceNormals[rndFace]
    print(rndFaceSel)
    NormalPos=rndFaceSel.split()[-2] 
    print(NormalPos)
    #Change buttons status
    cmds.button(MakeUI.MakeBtn,en=False,e=True)
    cmds.button(MakeUI.ResetBtn,en=True,e=True)
    cmds.button(MakeUI.ShadeBtn,en=True,e=True)
    cmds.button(MakeUI.EndrrBtn,en=True,e=True)
    
    #Reverse the plane if the normals are inverted   
    if(float(NormalPos)<0.4):
        cmds.polyNormal("RoadRiverBase",nm=0,unm=0,ch=1)  
    if (RoadOffset>0):
        cmds.move(RoadOffset, y=True)
    makingriver=cmds.checkBox(MakeUI.RiverCheck,q=True,v=True)
    if (makingriver):
        RiverOnly()

    
#Function to reset the created plane    
def ResetRoadRiver():
    cmds.select("RoadRiverBase")
    cmds.delete()
    #Change buttons status
    cmds.button(MakeUI.MakeBtn,en=True,e=True)
    cmds.button(MakeUI.ResetBtn,en=False,e=True)
    cmds.button(MakeUI.ShadeBtn,en=False,e=True)
    cmds.button(MakeUI.EndrrBtn,en=False,e=True)
    cmds.button(MakeUI.ShadeRiverBtn, e=True, en=False)

#Function to make the plane flat
def RiverOnly():
    #Convert selection to vertices and scale to flaten
    cmds.select("RoadRiverBase",r=True)
    cmds.ConvertSelectionToVertices()
    cmds.scale(1,0,1,r=True)
    cmds.button(MakeUI.ShadeRiverBtn,e=True,en=True)
    cmds.button(MakeUI.ShadeBtn,en=False,e=True)

#Function to rename and end the road/river
def endRivRoad():
    cmds.rename("RoadRiverBase",nameVar)
    #Change buttons status
    cmds.button(MakeUI.MakeBtn,en=True,e=True)
    cmds.button(MakeUI.ResetBtn,en=False,e=True)
    cmds.button(MakeUI.ShadeBtn,en=False,e=True)
    cmds.button(MakeUI.EndrrBtn,en=False,e=True)
    cmds.button(MakeUI.ShadeRiverBtn, e=True, en=False)

#Function to shade the road plane
def roadShader():
    #Create a shading node and other nodes that connect to it
    shader=cmds.shadingNode("blinn",asShader=True,n="RoadShader")
    file_node=cmds.shadingNode("file",asTexture=True,n="texture")
    BumpNode=cmds.shadingNode("bump2d",asUtility=True,n="Bump2dNode")
    file_nodeNM=cmds.shadingNode("file",asTexture=True,n="textureNM")
    UVPlacer=cmds.shadingNode("place2dTexture",asUtility=True,n="UVTiler")
    #Window for file selection
    texturefile=cmds.fileDialog2(cap="Choose texture file",fm=1)
    print (texturefile)
    file=(texturefile[0])
    texturefileNM=cmds.fileDialog2(cap="Choose Normal Map file",fm=1)
    print (texturefile)
    fileNM=(texturefileNM[0])
    #Create a shadding group
    shading_group=cmds.sets(renderable=True,nss=True,empty=True)
    #Connect files to the shadder
    cmds.setAttr(file_node+".fileTextureName",file,type="string")
    cmds.setAttr(file_nodeNM+".fileTextureName",fileNM,type="string")
    cmds.connectAttr("%s.outColor"%shader,"%s.surfaceShader"%shading_group)
    cmds.connectAttr("%s.outColor"%file_node,"%s.color"%shader)
    cmds.connectAttr("%s.outUV"%UVPlacer,"%s.uvCoord"%file_node)
    cmds.connectAttr("%s.outUV"%UVPlacer,"%s.uvCoord"%file_nodeNM)
    cmds.setAttr("%s.bumpInterp"%BumpNode,1)
    cmds.connectAttr("%s.outAlpha"%file_nodeNM,"%s.bumpValue"%BumpNode)
    cmds.connectAttr("%s.outNormal"%BumpNode,"%s.normalCamera"%shader)
    cmds.select("RoadRiverBase",r=True)    
    cmds.sets("RoadRiverBase",e=True,fe=shading_group)

#Function to shade the river plane    
def riverShader():
    #Create a shading node and other nodes that connect to it
    shader=cmds.shadingNode("blinn",asShader=True,n="RiverShader")
    file_node=cmds.shadingNode("file",asTexture=True,n="texture")
    BumpNode=cmds.shadingNode("bump2d",asUtility=True,n="Bump2dNode")
    file_nodeNM=cmds.shadingNode("file",asTexture=True,n="textureNM")
    UVPlacer=cmds.shadingNode("place2dTexture",asUtility=True,n="UVTiler2")
    print(UVPlacer)
    #Window for file selection
    texturefile=cmds.fileDialog2(cap="Choose texture file",fm=1)
    print (texturefile)
    file=(texturefile[0])
    texturefileNM=cmds.fileDialog2(cap="Choose Normal Map file",fm=1)
    print (texturefile)
    fileNM=(texturefileNM[0])
    #Create a shadding group
    shading_group=cmds.sets(renderable=True,nss=True,empty=True)
    #Connect files to the shadder
    cmds.setAttr(file_node+".fileTextureName",file,type="string")
    cmds.setAttr(file_nodeNM+".fileTextureName",fileNM,type="string")
    cmds.connectAttr("%s.outColor"%shader,"%s.surfaceShader"%shading_group)
    cmds.connectAttr("%s.outColor"%file_node,"%s.color"%shader)
    cmds.connectAttr("%s.outUV"%UVPlacer,"%s.uvCoord"%file_node)
    cmds.connectAttr("%s.outUV"%UVPlacer,"%s.uvCoord"%file_nodeNM)
    cmds.setAttr("%s.bumpInterp"%BumpNode,1)
    cmds.connectAttr("%s.outAlpha"%file_nodeNM,"%s.bumpValue"%BumpNode)
    cmds.connectAttr("%s.outNormal"%BumpNode,"%s.normalCamera"%shader)
    cmds.select("RoadRiverBase",r=True)    
    cmds.sets("RoadRiverBase",e=True,fe=shading_group)
    #Connect time node to move the shadder
    #Connects to the rotation of the uvs, for some reason connecting it to the offset wasn't working
    cmds.connectAttr("time1.outTime", UVPlacer+".rotateUV", f=True)
    cmds.confirmDialog(t="Shadder animation",m="Press play on the timeline to see shadder move",b="OK")

#THIS ARE THE FUNCTIONS FROM MY CAPSTONE
#Create a plane for the user to create a window
def WindowPlane():
    cmds.group(em=True,n="Window") 
    WindowPlane.windowSection=cmds.polyPlane(n='window01',w=10,h=10,sh=3,sw=3)    
    cmds.rotate(90,0,0)
    #Put it in a group to modify
    cmds.parent(WindowPlane.windowSection,"Window",r=False)
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeAttrFL,e=True,en=True,cl=False)
    cmds.button(MakeUI.createPlaneBtn,e=True,en=False)
    cmds.button(MakeUI.alreadyPlaneBtn,e=True,en=False)
    cmds.button(MakeUI.confirmPlaneBtn,e=True,en=False)
    cmds.button(MakeUI.makePlaneBtn,e=True,en=False)

#Delete the plane and go back
def DeletePlane():
    cmds.select("Window")
    cmds.delete()
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeAttrFL,edit=True,en=False,cl=True)
    cmds.button(MakeUI.createPlaneBtn,e=True,en=True)
    cmds.button(MakeUI.alreadyPlaneBtn,e=True,en=True)
#Get width of the plane from user  
def SectionsWidth():
    global userSectionWidth
    userSectionWidth=cmds.intSliderGrp(MakeUI.sectionWidth,v=True,q=True)
    cmds.setAttr(WindowPlane.windowSection[1]+'.width',userSectionWidth)
    print(userSectionWidth)
    cmds.button(MakeUI.confirmPlaneBtn,e=True,en=False)
    return userSectionWidth
    
#Get height of the plane from user
def SectionsHeight():
    global userSectionHeight
    userSectionHeight=cmds.intSliderGrp(MakeUI.sectionHeight,v=True,q=True)
    cmds.setAttr(WindowPlane.windowSection[1]+'.height',userSectionHeight)
    print(userSectionHeight)  
    cmds.button(MakeUI.confirmPlaneBtn,e=True,en=False)
    return userSectionHeight  
    
#Get plane subdivisions on x from the user
def WindowPlaneSubDivX():
    WindowPlaneSubDivX.userSectionSDx=cmds.intSliderGrp(MakeUI.sectionSDx,v=True,q=True)
    cmds.setAttr(WindowPlane.windowSection[1]+'.subdivisionsWidth',WindowPlaneSubDivX.userSectionSDx)
    cmds.button(MakeUI.confirmPlaneBtn,e=True,en=False)
#Get plane subdivisions on y from the user    
def WindowPlaneSubDivY():
    WindowPlaneSubDivY.userSectionSDy=cmds.intSliderGrp(MakeUI.sectionSDy,v=True,q=True)
    cmds.setAttr(WindowPlane.windowSection[1]+'.subdivisionsHeight',WindowPlaneSubDivY.userSectionSDy)
    cmds.button(MakeUI.confirmPlaneBtn,e=True,en=True)
#Confirm plane attributes
def ConfirmAttr():
    #Activate and deactivate sections
    cmds.intSliderGrp(MakeUI.sectionWidth,e=True,vis=False)
    cmds.intSliderGrp(MakeUI.sectionHeight,e=True,vis=False)
    cmds.intSliderGrp(MakeUI.sectionSDx,e=True,vis=False)
    cmds.intSliderGrp(MakeUI.sectionSDy,e=True,vis=False)  
    cmds.button(MakeUI.makePlaneBtn,e=True,en=True) 
    cmds.button(MakeUI.confirmPlaneBtn,e=True,en=False)
#Confirm window plane that the user created is done    
def WindowPlaneEnd():
    #Hide the group in the outliner
    cmds.hide("Window")
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeAttrFL,edit=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.planeFL,edit=True,en=False,cl=True)
    WindowPlane.windowSection=cmds.ls(sl=True)
    #Create a group if one doesn't exist
    if cmds.objExists("Window"):
        pass
    else:
        cmds.group(em=True,n="Window")
        cmds.parent(WindowPlane.windowSection,"Window",r=False)
    cmds.frameLayout(MakeUI.doorFL,edit=True,en=True,cl=False)
#Confirm window plane that already existed
def ExistingPlane():
    WindowPlaneSubDivY.userSectionSDy=3
    WindowPlaneSubDivX.userSectionSDx=3
    WindowPlane.windowSection=cmds.ls(sl=True)
    #Create a group if one doesn't exist
    if cmds.objExists("Window"):
        pass
    else:
        cmds.group(em=True,n="Window")
        cmds.parent(WindowPlane.windowSection,"Window",r=False)
    #Activate and deactivate sections
    cmds.button(MakeUI.createPlaneBtn,e=True,en=False)
    cmds.button(MakeUI.alreadyPlaneBtn,e=True,en=False)
    cmds.frameLayout(MakeUI.planeSizeFL,edit=True,en=True,cl=False)
    cmds.button(MakeUI.locBtn,e=True,en=True)
    cmds.button(MakeUI.deleteLocBtn,e=True,en=False)
    cmds.button(MakeUI.goBackBtn,e=True,en=True)
    cmds.button(MakeUI.locConfirm,e=True,en=False)
    
#Create locator for the user    
def Locators():
    Locators.topRightLoc=cmds.spaceLocator(n="TopRight")
    cmds.scale(5,5,5)
    cmds.move(10,10,0)
    Locators.bottomRightLoc=cmds.spaceLocator(n="BottomRight")
    cmds.scale(5,5,5)
    cmds.move(10,0,0)   
    Locators.bottomLeftLoc=cmds.spaceLocator(n="BottomLeft")
    cmds.scale(5,5,5)
    cmds.move(-10,0,0)  
    Locators.topLeftLoc=cmds.spaceLocator(n="TopLeft")
    cmds.scale(5,5,5)
    cmds.move(-10,10,0) 
    #Ask the user to place them
    cmds.confirmDialog(t="Place locators", m="Snap the locators to the corners of your the plane, press the confirm button when you're done.", b="OK")
    #Activate and deactivate sections
    cmds.button(MakeUI.locBtn,e=True,en=False)
    cmds.button(MakeUI.deleteLocBtn,e=True,en=True)
    cmds.button(MakeUI.goBackBtn,e=True,en=False)
    cmds.button(MakeUI.locConfirm,e=True,en=True)
#Get dimensions of the plane from the user    
def GetDimensions():
    #Get the width and height from the position of the locators
    cmds.select(Locators.topLeftLoc)
    topLeftLocPos=cmds.getAttr(".translateX")
    print(topLeftLocPos)
    cmds.select(Locators.topRightLoc)
    topRightLocPos=cmds.getAttr(".translateX")
    print(topRightLocPos)
    WidthLocDistance=abs(topRightLocPos-topLeftLocPos)
    print("the total width is: %s"%WidthLocDistance)
    cmds.select(Locators.bottomLeftLoc)
    bottomLeftLocPos=cmds.getAttr(".translateY")
    print(bottomLeftLocPos)
    cmds.select(Locators.topLeftLoc)
    topLeftLocPos=cmds.getAttr(".translateY")
    print(topLeftLocPos)
    HeigthLocDistance=abs(bottomLeftLocPos-topLeftLocPos)
    print("the total heigth is: %s"%HeigthLocDistance)
    #Delete the locators
    cmds.select(Locators.topLeftLoc)
    cmds.delete()
    cmds.select(Locators.bottomLeftLoc)
    cmds.delete()
    cmds.select(Locators.topRightLoc)
    cmds.delete()
    cmds.select(Locators.bottomRightLoc)
    cmds.delete()
    userSectionHeight=HeigthLocDistance
    print(userSectionHeight)
    userSectionWidth=WidthLocDistance
    print(userSectionWidth)
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeSizeFL,edit=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.planeFL,edit=True,en=False,cl=True)
    #Hide the group on the outliner
    cmds.hide("Window")
    cmds.frameLayout(MakeUI.doorFL,edit=True,en=True,cl=False)
#Delete locators       
def DeleteLoc():
    cmds.select(Locators.topLeftLoc)
    cmds.delete()
    cmds.select(Locators.bottomLeftLoc)
    cmds.delete()
    cmds.select(Locators.topRightLoc)
    cmds.delete()
    cmds.select(Locators.bottomRightLoc)
    cmds.delete()
    #Activate and deactivate sections
    cmds.button(MakeUI.locBtn,e=True,en=True)
    cmds.button(MakeUI.deleteLocBtn,e=True,en=False)
    cmds.button(MakeUI.goBackBtn,e=True,en=True)
    cmds.button(MakeUI.locConfirm,e=True,en=False)
#Go back to plane creation section        
def GoBack():
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeSizeFL,edit=True,en=False,cl=True)
    cmds.button(MakeUI.createPlaneBtn,e=True,en=True)
    cmds.button(MakeUI.alreadyPlaneBtn,e=True,en=True)
    cmds.parent(WindowPlane.windowSection,"Window",w=True)
    cmds.select("Window")
    cmds.delete()
    cmds.intSliderGrp(MakeUI.sectionWidth,e=True,vis=True)
    cmds.intSliderGrp(MakeUI.sectionHeight,e=True,vis=True)
    cmds.intSliderGrp(MakeUI.sectionSDx,e=True,vis=True)
    cmds.intSliderGrp(MakeUI.sectionSDy,e=True,vis=True)
#Create a plane for the user to create a door    
def DoorPlane():
    cmds.group(em=True,n="Door") 
    DoorPlane.doorSection=cmds.polyPlane(n='door01',w=userSectionWidth,h=userSectionHeight,sh=WindowPlaneSubDivY.userSectionSDy,sw=WindowPlaneSubDivX.userSectionSDx)    
    cmds.rotate(90,0,0)
    cmds.parent(DoorPlane.doorSection,"Door",r=False)
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeDoorFL,e=True,en=True,cl=False)
#A door plane already exists        
def ExistingDoor():
    DoorPlane.doorSection=cmds.ls(sl=True)
    #Create a group if one doesn't exists
    if cmds.objExists("Door"):
        pass
    else:
        cmds.group(em=True,n="Door")
        cmds.parent(DoorPlane.doorSection,"Door",r=False)
    cmds.hide("Door")
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.doorFL,edit=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.buildingFL,e=True,en=True,cl=False)
#Go back to previous section    
def DoorGoBack():
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.planeFL,edit=True,en=True,cl=False)
    cmds.frameLayout(MakeUI.doorFL,edit=True,en=False,cl=True)
    cmds.showHidden("Window")
    cmds.button(MakeUI.createPlaneBtn,e=True,en=True)
    cmds.button(MakeUI.alreadyPlaneBtn,e=True,en=True) 
    if cmds.objExists("Door"):
        cmds.delete("Door")
#Confirm door plane    
def DoorConfirm():
    DoorPlane.doorSection=cmds.ls(sl=True)
    if cmds.objExists("Door"):
        pass
    else:
        cmds.group(em=True,n="Door")
        cmds.parent(DoorPlane.doorSection,"Door",r=False)    
    cmds.hide("Door")
    #Activate and deactivate sections
    cmds.frameLayout(MakeUI.doorFL,edit=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.planeDoorFL,e=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.buildingFL,e=True,en=True,cl=False)
    cmds.intSliderGrp(MakeUI.buildingWidth,e=True,en=True)
    cmds.intSliderGrp(MakeUI.buildingDepth,e=True,en=True)
#Go back to door creation    
def DoorGoBack2():   
    cmds.frameLayout(MakeUI.planeDoorFL,e=True,en=False,cl=True)
    cmds.select("Door")
    cmds.delete()
#Go back to door section
def GoBackMod(): 
    cmds.frameLayout(MakeUI.doorFL,e=True,en=True,cl=False)
    cmds.frameLayout(MakeUI.buildingFL,e=True,en=False,cl=True)
    cmds.showHidden("Door")
    if cmds.objExists("WallsW"):
        cmds.delete("WallsW")
    if cmds.objExists("WallsD"):
        cmds.delete("WallsD")
    
    
#Set the width of the building
def BuildingWidth():
    lastOBJ=1
    #Get attributes from user
    BuildingWidth.SubDX=cmds.intSliderGrp(MakeUI.sectionSDx,v=True,q=True)
    BuildingWidth.SubDY=cmds.intSliderGrp(MakeUI.sectionSDy,v=True,q=True)    
    BuildingWidth.userBuildingWidth=cmds.intSliderGrp(MakeUI.buildingWidth,v=True,q=True)
    #Loop to modify the width everytime the user changes it
    if cmds.objExists("WallsW"):
        #Delete the group if already exists
        cmds.select("WallsW")
        cmds.delete()
        #Create a new group
        ParentGroup=cmds.group(em=True,n="WallsW")
        #Duplicate and move the plane to get the desired width
        for obj in range(0,BuildingWidth.userBuildingWidth):  
            BuildingWidth.wallW=cmds.polyPlane(n="WallW"+str(lastOBJ),w=userSectionWidth,h=userSectionHeight,sx=BuildingWidth.SubDX,sy=BuildingWidth.SubDY)
            cmds.parent("WallW"+str(lastOBJ),"WallsW",r=False)
            cmds.rotate(90,0,0)
            lastOBJ+=1
            cmds.move((userSectionWidth*obj)+userSectionWidth/2,0,0)
    else: 
        #If the group doesn't exist, runs without deleting it first 
        ParentGroup=cmds.group(em=True,n="WallsW")
        for obj in range(0,BuildingWidth.userBuildingWidth):     
            BuildingWidth.wallW=cmds.polyPlane(n="WallW"+str(lastOBJ),w=userSectionWidth,h=userSectionHeight,sx=BuildingWidth.SubDX,sy=BuildingWidth.SubDY)
            cmds.parent("WallW"+str(lastOBJ),"WallsW",r=False)
            cmds.rotate(90,0,0)
            lastOBJ+=1
            cmds.move((userSectionWidth*obj)+userSectionWidth/2,0,0)

        

def BuildingDepth():
    lastOBJ=1

    BuildingDepth.userBuildingDepth=cmds.intSliderGrp(MakeUI.buildingDepth,v=True,q=True)
    #Loop to modify the depth everytime the user changes it
    if cmds.objExists("WallsD"):
        #Delete the group if already exists
        cmds.select("WallsD")
        cmds.delete()    
        #Create a new group
        ParentGroup=cmds.group(em=True,n="WallsD")
        #Duplicate and move the plane to get the desired depth
        for obj in range(0,BuildingDepth.userBuildingDepth):
            BuildingDepth.wallD=cmds.polyPlane(n="WallD"+str(lastOBJ),w=userSectionWidth,h=userSectionHeight,sx=BuildingWidth.SubDX,sy=BuildingWidth.SubDY)
            cmds.parent("WallD"+str(lastOBJ),"WallsD",r=False)
            cmds.rotate(90,-90,0)
            lastOBJ+=1
            cmds.move(0,0,-(userSectionWidth*obj)+(-userSectionWidth/2))
    #If the group doesn't exist, runs without deleting it first
    else:
        ParentGroup=cmds.group(em=True,n="WallsD")
        for obj in range(0,BuildingDepth.userBuildingDepth):
            BuildingDepth.wallD=cmds.polyPlane(n="WallD"+str(lastOBJ),w=userSectionWidth,h=userSectionHeight,sx=BuildingWidth.SubDX,sy=BuildingWidth.SubDY)
            cmds.parent("WallD"+str(lastOBJ),"WallsD",r=False)
            cmds.rotate(90,-90,0)
            lastOBJ+=1
            cmds.move(0,0,-(userSectionWidth*obj)+(-userSectionWidth/2))

#Confirm the width and depth of the builsing
def ConfirmWD():
    WallVar=1
    #Create a new group
    cmds.group(em=True,n="Bottom")
    #Select old group
    DepthGrp=cmds.select("WallsD")
    DepthOBJ=cmds.listRelatives()
    print(len(DepthOBJ))
    DepthLen=len(DepthOBJ)+1
    #Get objects from previous groups, change their name and put under new group
    for i in range(1,DepthLen):
        cmds.select("WallD"+str(i))
        cmds.rename("WallD"+str(i),"Wall"+str(WallVar))
        cmds.parent(w=True)
        cmds.parent("Wall"+str(WallVar),"Bottom")
        WallVar+=1
    #Delete empty group
    cmds.delete("WallsD")    
    #Select old group    
    WidthGrp=cmds.select("WallsW")
    WidthOBJ=cmds.listRelatives()
    WidthLen=len(WidthOBJ)+1
    #Rename and move objects
    for i in range(1,WidthLen):
        cmds.select("WallW"+str(i))
        cmds.rename("WallW"+str(i),"Wall"+str(WallVar))
        cmds.parent(w=True)
        cmds.parent("Wall"+str(WallVar),"Bottom")
        WallVar+=1
        #delete old group
    cmds.delete("WallsW")
    #Activate and deactivate sections
    cmds.intSliderGrp(MakeUI.buildingWidth,e=True,en=False)
    cmds.intSliderGrp(MakeUI.buildingDepth,e=True,en=False)
    cmds.button(MakeUI.ConfirmWD,e=True,en=False)
    cmds.intSliderGrp(MakeUI.buildingHeight,e=True,en=True)
    cmds.button(MakeUI.GoBackHeight,e=True,en=True)
    cmds.button(MakeUI.MakeBuilding,e=True,en=True)

#Get the height of the building    
def BuildingHeight():
    lastOBJ=1
    BuildingHeight.userBuildingHeight=cmds.intSliderGrp(MakeUI.buildingHeight,v=True,q=True)
    #Delete if the group exists
    if cmds.objExists("WallsH"):
        cmds.select("WallsH")
        cmds.delete()    
        ParentGroup=cmds.group(em=True,n="WallsH")
        cmds.select("Bottom")
        WidthOBJ=cmds.listRelatives()
        WidthLen=len(WidthOBJ)+1
        #Get position of width and depth planes 
        for i in range(1,WidthLen):
            cmds.select("Wall"+str(i))
            wallX=cmds.getAttr("Wall"+str(i)+".translateX")
            wallY=cmds.getAttr("Wall"+str(i)+".translateY")
            wallZ=cmds.getAttr("Wall"+str(i)+".translateZ")
            #Duplicate planes to match height from user
            for obj in range(1,BuildingHeight.userBuildingHeight):
                tempObj=cmds.duplicate()
                cmds.parent(tempObj[0],w=True)
                cmds.setAttr(tempObj[0]+".translateX",wallX)
                cmds.setAttr(tempObj[0]+".translateY",wallY+userSectionHeight*obj)
                cmds.setAttr(tempObj[0]+".translateZ",wallZ)
                cmds.parent(tempObj[0],"WallsH")                
    #Run if the group doesn't exist    
    else:
        ParentGroup=cmds.group(em=True,n="WallsH")
        cmds.select("Bottom")
        WidthOBJ=cmds.listRelatives()
        WidthLen=len(WidthOBJ)+1
        for i in range(1,WidthLen):
            cmds.select("Wall"+str(i))        
            wallX=cmds.getAttr("Wall"+str(i)+".translateX")
            wallY=cmds.getAttr("Wall"+str(i)+".translateY")
            wallZ=cmds.getAttr("Wall"+str(i)+".translateZ")        
            for obj in range(1,BuildingHeight.userBuildingHeight):
                tempObj=cmds.duplicate()
                cmds.parent(tempObj[0],w=True)
                cmds.setAttr(tempObj[0]+".translateX",wallX)
                cmds.setAttr(tempObj[0]+".translateY",wallY+userSectionHeight*obj)
                cmds.setAttr(tempObj[0]+".translateZ",wallZ)
                cmds.parent(tempObj[0],"WallsH")

#Go back to width/depth section        
def GoBackHeight():
    if cmds.objExists("WallsH"):
        cmds.delete("WallsH")
    cmds.delete("Bottom")
    #Activate and deactivate sections
    cmds.intSliderGrp(MakeUI.buildingWidth,e=True,en=True)
    cmds.intSliderGrp(MakeUI.buildingDepth,e=True,en=True)
    cmds.button(MakeUI.ConfirmWD,e=True,en=True)
    cmds.intSliderGrp(MakeUI.buildingHeight,e=True,en=False)
    cmds.button(MakeUI.GoBackHeight,e=True,en=False)
    cmds.button(MakeUI.MakeBuilding,e=True,en=False)

#Confirm walls of the building
def ConfirmBuild():
    #Create new group
    cmds.group(em=True,n="Building")   
    #Select old group and duplicate
    cmds.select("Bottom")
    BottomGrp=cmds.ls(sl=True)
    BottomGrpDup=cmds.duplicate()
    #Move duplicate to new position
    cmds.move(userSectionWidth*BuildingWidth.userBuildingWidth,0,-userSectionWidth*BuildingDepth.userBuildingDepth)
    cmds.rotate(0,-180,0) 
     #Select old group and duplicate 
    cmds.select("WallsH")
    HeightGrp=cmds.ls(sl=True)
    HeightGrpDup=cmds.duplicate()
    #Move duplicate to new position
    cmds.move(userSectionWidth*BuildingWidth.userBuildingWidth,0,-userSectionWidth*BuildingDepth.userBuildingDepth)
    cmds.rotate(0,-180,0) 
    #Name var to match the objects that already exist
    nameVar=(BuildingDepth.userBuildingDepth+BuildingWidth.userBuildingWidth)*(BuildingHeight.userBuildingHeight)+1
    #Loops to change the name of the duplicates and parent under new group   
    for i in range(1,len(BottomGrpDup)):
        TempBottom=BottomGrpDup[i]
        cmds.rename("Bottom1|Wall"+str(i), "Wall"+str(nameVar))
        cmds.parent("Wall"+str(nameVar),w=True)
        cmds.parent("Wall"+str(nameVar),"Building")    
        nameVar=nameVar+1
    cmds.delete("Bottom1")    
    for i in range(1,len(BottomGrpDup)):
        cmds.parent("Wall"+str(i),w=True)
        cmds.parent("Wall"+str(i),"Building")
    cmds.delete("Bottom")    
    tempVar=len(BottomGrpDup)   
    for i in range(1,len(HeightGrpDup)):
        tempHeight=HeightGrpDup[i]
        cmds.rename("WallsH1|Wall"+str(tempVar), "Wall"+str(nameVar))
        cmds.parent("Wall"+str(nameVar),w=True)
        cmds.parent("Wall"+str(nameVar),"Building")
        tempVar+=1
        nameVar+=1
    cmds.delete("WallsH1")    
    tempVar=len(BottomGrpDup)
    for i in range(1,len(HeightGrpDup)):
        cmds.parent("Wall"+str(tempVar),w=True)
        cmds.parent("Wall"+str(tempVar),"Building")
        tempVar+=1
    cmds.delete("WallsH")
    #Activate and deactivate sections   
    cmds.intSliderGrp(MakeUI.buildingHeight,e=True,en=False)
    cmds.button(MakeUI.MakeBuilding,e=True,en=False)
    cmds.button(MakeUI.GoBackHeight,e=True,en=False)
    cmds.button(MakeUI.GoBackBuilding,e=True,en=True)
    cmds.frameLayout(MakeUI.buildingFL,edit=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.finalize,e=True,en=True,cl=False)    
#Go back to width/depth/height section
def GoBackBuild():
    cmds.delete("Building")
    #Activate and deactivate sections
    cmds.intSliderGrp(MakeUI.buildingWidth,e=True,en=True)
    cmds.intSliderGrp(MakeUI.buildingDepth,e=True,en=True)
    cmds.button(MakeUI.ConfirmWD,e=True,en=True)
    cmds.frameLayout(MakeUI.buildingFL,edit=True,en=True,cl=False)
    cmds.frameLayout(MakeUI.finalize,e=True,en=False,cl=True)
#Add planes to the windows list  
def addSelectionW():
    selectedOBJs=cmds.ls(sl=True,o=True)
    for i in selectedOBJs:
        cmds.textScrollList(MakeUI.SLObjList,e=True,a=i)
        print ("the selected objs are:"+ str(selectedOBJs))
    cmds.select(cl=True)
#Remove planes from the windows list    
def RemSelectionW():
    selectedPanel=cmds.textScrollList(MakeUI.SLObjList,q=True,si=1)
    cmds.textScrollList(MakeUI.SLObjList,e=True,ri=selectedPanel)    
#Make selection of the planes from the list
def SelectPlanes():
    global selectedPanels
    selectedPanels=cmds.textScrollList(MakeUI.SLObjList,q=True,si=1)
    print ("user selected this object: "+selectedPanels[0])
    return selectedPanels
#Place window on the selected positions        
def PlaceWindows(): 
    #Make new group
    ParentGroup=cmds.group(em=True,n="Windows")
    #Get positions of selected planes and place duplicates of the window over
    for i in range(0,len(selectedPanels)):
        print(selectedPanels)
        cmds.select(selectedPanels[i])
        #Get position and rotation
        panelPosT=cmds.xform(selectedPanels[i], q=True, ws=True, t=True)
        panelPosR=cmds.xform(selectedPanels[i], q=True, ws=True,  ro=True)
        cmds.select("Window")
        #Make new object
        cmds.duplicate(n="Window"+str(i))
        #Place on the position
        cmds.setAttr("Window"+str(i)+'.translateX',panelPosT[0])
        cmds.setAttr("Window"+str(i)+'.translateY',panelPosT[1])
        cmds.setAttr("Window"+str(i)+'.translateZ',panelPosT[2])
        #rotate to match
        cmds.setAttr("Window"+str(i)+'.rotateX',panelPosR[0]-90)
        cmds.setAttr("Window"+str(i)+'.rotateY',panelPosR[1])
        cmds.setAttr("Window"+str(i)+'.rotateZ',panelPosR[2])        
        cmds.select("Window"+str(i))        
        GrpWin=cmds.listRelatives()
        Grplen=len(GrpWin)
        print(GrpWin)
        #change name on objects and parent under new group
        for obj in range(0,Grplen):
            cmds.parent("Window"+str(i)+"|"+GrpWin[obj],w=True)
            cmds.rename("|"+GrpWin[obj],"Win"+str(i))
            cmds.parent("Win"+str(i),"Windows")
            cmds.delete("Window"+str(i))
        #unhide group
        cmds.showHidden("Windows")   
        #Activate and deactivate sections   
        cmds.button(MakeUI.addWindows,e=True,en=False)
        cmds.button(MakeUI.remWindows,e=True,en=False)
        cmds.textScrollList(MakeUI.SLObjList,e=True,en=False)  
        cmds.button(MakeUI.makeWindows,e=True,en=False)
        cmds.button(MakeUI.backWindows,e=True,en=True)
        cmds.frameLayout(MakeUI.finalizeDoor,e=True,en=True,cl=False)
        cmds.frameLayout(MakeUI.finalizeWin,e=True,en=False,cl=True)
#Go back to selection from the list
def GoBackWindows():
    #Activate and deactivate sections
    cmds.button(MakeUI.addWindows,e=True,en=True)
    cmds.button(MakeUI.remWindows,e=True,en=True)
    cmds.textScrollList(MakeUI.SLObjList,e=True,en=True)  
    cmds.button(MakeUI.makeWindows,e=True,en=True)
    cmds.button(MakeUI.backWindows,e=True,en=False)
    cmds.frameLayout(MakeUI.finalizeDoor,e=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.finalizeWin,e=True,en=True,cl=False)
    cmds.button(MakeUI.GoBackBuilding,e=True,en=True)
    #Delete if the group exists
    if cmds.objExists("Windows"):
        cmds.delete("Windows")
#Add planes to door list    
def addSelectionD():
    selectedOBJs=cmds.ls(sl=True,o=True)
    for i in selectedOBJs:
        cmds.textScrollList(MakeUI.SLObjListD,e=True,a=i)
        print ("the selected objs are:"+ str(selectedOBJs))
    cmds.select(cl=True)
#Remove planes from door list    
def RemSelectionD():
    selectedPanel=cmds.textScrollList(MakeUI.SLObjListD,q=True,si=1)
    cmds.textScrollList(MakeUI.SLObjListD,e=True,ri=selectedPanel)    
#Select planes from door list
def SelectPlanesDoor():
    global selectedPanelsD
    selectedPanelsD=cmds.textScrollList(MakeUI.SLObjListD,q=True,si=1)
    print ("user selected this object: "+selectedPanelsD[0])
    return selectedPanelsD
#Place door on selected postions    
def PlaceDoor():  
    #Create new group
    ParentGroup=cmds.group(em=True,n="Doors")
    #Get positions of selected planes
    for i in range(0,len(selectedPanelsD)):
        print(selectedPanelsD)
        cmds.select(selectedPanelsD[i])
        #Get translate and rotate
        panelPosT=cmds.xform(selectedPanelsD[i], q=True, ws=True, t=True)
        panelPosR=cmds.xform(selectedPanelsD[i], q=True, ws=True,  ro=True)
        #Duplicate Door
        cmds.select("Door")
        cmds.duplicate(n="Door"+str(i))
        #Set attributes
        cmds.setAttr("Door"+str(i)+'.translateX',panelPosT[0])
        cmds.setAttr("Door"+str(i)+'.translateY',panelPosT[1])
        cmds.setAttr("Door"+str(i)+'.translateZ',panelPosT[2])
        cmds.setAttr("Door"+str(i)+'.rotateX',panelPosR[0]-90)
        cmds.setAttr("Door"+str(i)+'.rotateY',panelPosR[1])
        cmds.setAttr("Door"+str(i)+'.rotateZ',panelPosR[2])
        cmds.select("Door"+str(i))
        GrpDoor=cmds.listRelatives()
        Grplen=len(GrpDoor)
        print(GrpDoor)
        #change name and parent under new group
        for obj in range(0,Grplen):
            cmds.parent("Door"+str(i)+"|"+GrpDoor[obj],w=True)
            cmds.rename("|"+GrpDoor[obj],"Dr"+str(i))
            cmds.parent("Dr"+str(i),"Doors")
            cmds.delete("Door"+str(i))   
        #unhide group
        cmds.showHidden("Doors")  
        #Activate and deactivate sections
        cmds.button(MakeUI.addDoor,e=True,en=False)
        cmds.button(MakeUI.remDoor,e=True,en=False)
        cmds.textScrollList(MakeUI.SLObjListD,e=True,en=False)  
        cmds.button(MakeUI.makeDoor,e=True,en=False)
        cmds.button(MakeUI.backDoor,e=True,en=True)
        cmds.button(MakeUI.backWindows,e=True,en=False)
        cmds.button(MakeUI.finishBuilding,e=True,en=True)
#Go back to lsit selection for the door
def GoBackDoor():
    #Activate and deactivate sections
    cmds.button(MakeUI.addDoor,e=True,en=True)
    cmds.button(MakeUI.remDoor,e=True,en=True)
    cmds.textScrollList(MakeUI.SLObjListD,e=True,en=True)  
    cmds.button(MakeUI.makeDoor,e=True,en=True)
    cmds.button(MakeUI.backDoor,e=True,en=False)
    cmds.button(MakeUI.backWindows,e=True,en=True)
    cmds.button(MakeUI.finishBuilding,e=True,en=False)
    #delete the group if it exists
    if cmds.objExists("Doors"):
        cmds.delete("Doors")            
#Finalize the building        
def FinishBuilding():
    #Parent everything under one group and move to place over the grid
    cmds.group(em=True,n="FinalBuilding")
    cmds.parent("Windows","FinalBuilding")
    cmds.move(0,userSectionHeight/2,0)
    cmds.parent("Doors","FinalBuilding")
    cmds.move(0,userSectionHeight/2,0)
    cmds.parent("Building","FinalBuilding")
    cmds.move(0,userSectionHeight/2,0)
    cmds.select("FinalBuilding")
    #Delete panels that wont be used
    cmds.delete(selectedPanelsD)
    cmds.delete(selectedPanels)
    #Create the roof and place
    roofWidth=userSectionWidth*BuildingWidth.userBuildingWidth
    roofDepth=userSectionWidth*BuildingDepth.userBuildingDepth
    roofHeight=userSectionHeight*BuildingHeight.userBuildingHeight
    cmds.polyPlane(n="Roof",sx=1,sy=1,w=roofWidth,h=roofDepth)
    cmds.move(roofWidth/2,roofHeight,-roofDepth/2)
    cmds.parent("Roof","FinalBuilding")
    cmds.frameLayout(MakeUI.finalize,e=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.finalizeDoor,e=True,en=False,cl=True)
    cmds.frameLayout(MakeUI.planeFL,edit=True,en=True,cl=False)
