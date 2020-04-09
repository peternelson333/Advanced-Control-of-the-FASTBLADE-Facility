% Peter Nelson 02/10/19
% This code automates the process of data wrangling outputs from
% FASTBLADE's Simulink model to CSVs.


clc
clear

path = "C:\Users\Peter's 2nd Laptop\University of Edinburgh\FASTBLADE Students - Documents\Peter Nelson\Controlled Copy 10 Direct connection\Data\3rd Upload\";

extension=('*.mat');
fileloc=strcat(path,extension);

format long

DATA=dir(fileloc);
report = [];
files=length(DATA);

for u = 1:files
    filename=DATA(u,1).name;
    
        load(filename)
        eval(['data = ' filename(1:end-4)])
        
        
%% METADATA      
        data2.model=data.MetaData.Model;
        data2.nbp=data.MetaData.nbp;
        data2.simLength=data.MetaData.SimLength;
        data2.cycleTime=data.MetaData.CycleTime;
        data2.realTime=data.MetaData.Realtime;
        data2.sampleRate=data.MetaData.SampleRate;
        data2.inputAmp=data.MetaData.InputAmp;
        data2.inputBias=data.MetaData.InputBias;
        data2.viscous=data.MetaData.Viscous;
        data2.movAvLength=data.MetaData.movAvLength;
        data2.preload=data.MetaData.preload;
        data2.gravity=data.MetaData.Gravity;
        data2.signal=data.MetaData.Signal;
        
        data2.InputFreq=data.MetaData.Input_Variables.inputFreq;
        data2.force=data.MetaData.Input_Variables.Force;
        data2.Rvalue=data.MetaData.Input_Variables.Rvalue;
        data2.wavetype=data.MetaData.Input_Variables.Wavetype;
        data2.control_mode=data.MetaData.Input_Variables.control_mode;
        data2.pid_p=data.MetaData.Input_Variables.pid_p;
        data2.pid_d=data.MetaData.Input_Variables.pid_d;
        data2.controlPower=data.MetaData.Input_Variables.controlPower;
        data2.massCoef=data.MetaData.Input_Variables.massCoef;
        data2.StiffCoef=data.MetaData.Input_Variables.stiffCoef;
        data2.Npumps=data.MetaData.Input_Variables.npumps;
        data2.Nrams=data.MetaData.Input_Variables.nrams;
        data2.pRadius=data.MetaData.Input_Variables.pRadius;
        data2.rRadius=data.MetaData.Input_Variables.rRadius;
        data2.gain=data.MetaData.Input_Variables.Gain;
        data2.rotational_inertia_kgm2=data.MetaData.Input_Variables.Rotational_inertia_kgm2;
        data2.torque_control_gain=data.MetaData.Input_Variables.Torque_control_gain;
        
 
%BLADE PARAMS
        for k = 1:data.MetaData.Input_Variables.nrams
            data2.(sprintf('bladePushed%d', k)) = data.MetaData.BladeParams.Pushed(k);
        end     
        
              
        for k = 1:data.MetaData.nbp
            data2.(sprintf('bladeHeight%d', k)) = data.MetaData.BladeParams.height(k);
            data2.(sprintf('bladepLR%d', k)) = data.MetaData.BladeParams.pLR(k);
            data2.(sprintf('bladeLength%d', k)) = data.MetaData.BladeParams.length(k);
           data2.(sprintf('bladeThick%d', k)) = data.MetaData.BladeParams.thick(k);
            data2.(sprintf('bladeMass%d', k)) = data.MetaData.BladeParams.mass(k);  
        end
        
% CYL PARAMS
        for k = 1:data.MetaData.Input_Variables.nrams
            data2.(sprintf('cylrPiston%d', k)) = data.MetaData.CylParams.rPiston(k); 
            data2.(sprintf('cylrRod%d', k)) = data.MetaData.CylParams.rRod(k); 
            data2.(sprintf('cylrStroke%d', k)) = data.MetaData.CylParams.stroke(k); 
            data2.(sprintf('cylMass%d', k)) = data.MetaData.CylParams.mass(k); 
            data2.(sprintf('cylInitPres%d', k)) = data.MetaData.CylParams.initPres(k); 
            data2.(sprintf('cylInitPos%d', k)) = data.MetaData.CylParams.initPos(k); 
        end

%HYD SYS PARAMS
        data2.hydSys_System_stiffness_barpcc=data.MetaData.HydSys.System_stiffness_barpcc;
        data2.hydSys_LPF_freq=data.MetaData.HydSys.LPF_freq;
        data2.hydSys_DDP_cc=data.MetaData.HydSys.DDP_cc;
        data2.hydSys_MDF_pump=data.MetaData.HydSys.MDF_pump;
        data2.hydSys_MDF_motor=data.MetaData.HydSys.MDF_motor;
        data2.hydSys_Motor_power_limit_kW=data.MetaData.HydSys.Motor_power_limit_kW;
        data2.hydSys_Rotational_inertia_kgm2=data.MetaData.HydSys.Rotational_inertia_kgm2;
        data2.hydSys_Torque_control_gain=data.MetaData.HydSys.Torque_control_gain;
        data2.hydSys_DDPM_Disp_ccprev=data.MetaData.HydSys.DDPM_Disp_ccprev;
        
%PIPES PARAMS
        data2.pipes_mainLength=data.MetaData.Pipes.mainLength;
        data2.pipes_mainDiam=data.MetaData.Pipes.mainDiam;
        data2.pipes_Segments=data.MetaData.Pipes.Segments;
        data2.pipes_interlinkLength=data.MetaData.Pipes.interlinkLength;
        data2.pipes_interlinkDiam=data.MetaData.Pipes.interlinkDiam;
        data2.pipes_flexLength=data.MetaData.Pipes.flexLength;
        data2.pipes_flexDiam=data.MetaData.Pipes.flexDiam;
        
%PISTON PARAMS
        data2.pistonStroke=data.MetaData.Piston.pStroke;
        data2.pistonMass=data.MetaData.Piston.pMass;
        data2.pistoninitPres=data.MetaData.Piston.initPres;
        data2.pistonGenInitPos=data.MetaData.Piston.genInitPos;
        data2.pistonTotalAcumVol=data.MetaData.Piston.TotalAcumVol;
        data2.pistonMinGasVol=data.MetaData.Piston.MinGasVol;
        data2.pistonAccumLiquidVol=data.MetaData.Piston.AccumLiquidVol;
        
%ELAST PARAMS
        for k = 1:data.MetaData.nbp
            data2.(sprintf('damp%d', k)) = data.MetaData.ElastParams.damp(k);
            data2.(sprintf('stiff%d', k)) = data.MetaData.ElastParams.stiff(k); 
        end

 
% Command stuff 
        data2.sampleDelay=data.Command.SampleDelay;
        data2.timeDelay=data.Command.TimeDelay;
        data2.phaseLag=data.Command.PhaseLag;
        data2.scSdev1=data.Command.SigComp.sdev1;
        data2.scSdev2=data.Command.SigComp.sdev2;
        data2.scU1=data.Command.SigComp.u1;
        data2.scU2=data.Command.SigComp.u2;
        data2.scR2=data.Command.SigComp.r2;
        data2.scLSQ=data.Command.SigComp.lsq;
        data2.scLag=data.Command.SigComp.lag;
        data2.scLagtime=data.Command.SigComp.lagtime;
        data2.scP1= data.Command.SigComp.p(1);
        data2.scP2= data.Command.SigComp.p(2);
        
        
 
%% TIMESERIES DATA
        data3.DataTime = data.Time;     
       
%COMMAND PARAMS
        data3.DesiredLoad=data.Command.Desired;
        data3.RecordedLoad=4.*data.Command.Measured;
        
%HYDRAULIC LINE PARAMS
        data3.crossFlow1=data.HydraulicLine(1).CrossFlow;
        data3.crossFlow2=data.HydraulicLine(3).CrossFlow;
        data3.crossFlow3=data.HydraulicLine(3).CrossFlow;
        
%PUMP PARAMS
        for k = 1:data.MetaData.Input_Variables.nrams
            data3.(sprintf('pumpRPM%d', k)) = data.Pump(k).RPM; 
            data3.(sprintf('pumpMotTorq%d', k)) = data.Pump(k).MotTorq; 
            data3.(sprintf('pumpDDP%d', k)) = data.Pump(k).DDP;
            data3.(sprintf('pumpPower%d', k)) = data.Pump(k).Power;
            data3.(sprintf('pumpFlowrate%d', k)) = data.Pump(k).Flowrate;
            data3.(sprintf('pumpThrottle%d', k)) = data.Pump(k).Throttle;
        end
        
%CYL PARAMS
        for k = 1:data.MetaData.Input_Variables.nrams
            data3.(sprintf('cylForce%d', k)) = data.Cylinder(k).Force; 
            data3.(sprintf('cylPressure%d', k)) = data.Cylinder(k).Pressure; 
            data3.(sprintf('cylPosition%d', k)) = data.Cylinder(k).Position;
            data3.(sprintf('cylVelocity%d', k)) = data.Cylinder(k).Velocity;
            data3.(sprintf('cylAccel%d', k)) = data.Cylinder(k).Accel;
            data3.(sprintf('cylMoment%d', k)) = data.Cylinder(k).Moment;
            data3.(sprintf('cylFlowrate%d', k)) = data.Cylinder(k).Flowrate;
        end

%BODY PARAMS
        for k = 1:data.MetaData.nbp
            data3.(sprintf('bodyAngle%d', k)) = data.Body(k).Angle;
            data3.(sprintf('bodyVelocity%d', k)) = data.Body(k).Velocity; 
            data3.(sprintf('bodyAccel%d', k)) = data.Body(k).Accel;
            data3.(sprintf('bodyPosition%d', k)) = data.Body(k).Position;
        end

        
%TOTAL PARAMS
        data3.total_Moment=data.Total.Moment;
        data3.total_Flowrate=data.Total.Flowrate;
        data3.total_Power=data.Total.Power;
        
 
        %REORDER STRUCTURES
        data2=orderfields(data2);
        data3=orderfields(data3);
        
        
        
        struct2csv(data2,[filename(1:end-4) '_meta.csv'])                       
        struct2csv(data3,[filename(1:end-4) '.csv'])          
        fclose all
         
end
