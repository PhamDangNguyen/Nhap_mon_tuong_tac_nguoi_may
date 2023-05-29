%%
clc
clear
close all
% Link length- can be changed  % length of first arm  % length of second arm % length of third arm
d1=0.5;
d2=0.7;
d3=0.6;
d4=0.2;
d5=0.15;
d6 = 0.15;
hold('on')
% Axis Properties
X=[0 0 d2 d2+d3 d2+d3 d2+d3 d2+d3];
Y=[0 0 0 0 d4 d4 d4+d6];
Z=[0 d1 d1 d1 d1 d1-d5 d1-d5];
Tool = plot3(X,Y,Z,'ro-','LineWidth',4,'XDataSource','X','YDataSource','Y','ZDataSource','Z');
axis([-2 2 -2 2 0 2]);
set(gca,'DataAspectRatio',[1 1 1])
grid on
hold('on')

xlabel('X(m)')
ylabel('Y(m)')
zlabel('Z(m)')
%doannay chua lam gi con doan trenchuan det roi
q1= pi/2;
q2= -pi/5;
q3= pi/6;
q4= pi/2;
q5= pi/3;
q6= pi/3;


% Ve quy dao cua 5 khau
X0=0;
X1=0;
X2=0;
X3=(cos(q1) * cos(q2) - sin(q1) * sin(q2)) * d2 * cos(q3);
X4= 0.2e1 * cos(q1) * cos(q2) * cos(q3) ^ 2 * cos(q4) * d3 - 0.2e1 * cos(q1) * cos(q2) * cos(q3) * sin(q3) * sin(q4) * d3 - 0.2e1 * sin(q1) * sin(q2) * cos(q3) ^ 2 * cos(q4) * d3 + 0.2e1 * sin(q1) * sin(q2) * cos(q3) * sin(q3) * sin(q4) * d3 + 0.2e1 * cos(q1) * cos(q2) * cos(q3) ^ 2 * d2 - 0.2e1 * sin(q1) * sin(q2) * cos(q3) ^ 2 * d2 + cos(q1) * cos(q2) * cos(q3) * d2 - cos(q1) * cos(q2) * cos(q4) * d3 - sin(q1) * sin(q2) * cos(q3) * d2 + sin(q1) * sin(q2) * cos(q4) * d3 - cos(q1) * cos(q2) * d2 + cos(q1) * sin(q2) * d4 + cos(q2) * sin(q1) * d4 + sin(q1) * sin(q2) * d2;
X5=cos(q1) * cos(q2) * cos(q3) * cos(q4) * d3 - cos(q1) * cos(q2) * sin(q3) * sin(q4) * d3 - sin(q1) * sin(q2) * cos(q3) * cos(q4) * d3 + sin(q1) * sin(q2) * sin(q3) * sin(q4) * d3 + cos(q1) * cos(q2) * cos(q3) * d2 - sin(q1) * sin(q2) * cos(q3) * d2 + cos(q1) * sin(q2) * d4 + cos(q1) * sin(q2) * d5 + cos(q2) * sin(q1) * d4 + cos(q2) * sin(q1) * d5;
X6= -cos(q1) * cos(q2) * sin(q5) * sin(q3) * sin(q4) * d6 + cos(q1) * cos(q2) * sin(q5) * cos(q4) * cos(q3) * d6 + cos(q1) * cos(q2) * cos(q5) * sin(q3) * cos(q4) * d6 + cos(q1) * cos(q2) * cos(q5) * cos(q3) * sin(q4) * d6 + sin(q1) * sin(q2) * sin(q5) * sin(q3) * sin(q4) * d6 - sin(q1) * sin(q2) * sin(q5) * cos(q4) * cos(q3) * d6 - sin(q1) * sin(q2) * cos(q5) * sin(q3) * cos(q4) * d6 - sin(q1) * sin(q2) * cos(q5) * cos(q3) * sin(q4) * d6 - cos(q1) * cos(q2) * sin(q3) * sin(q4) * d3 + cos(q1) * cos(q2) * cos(q4) * cos(q3) * d3 + sin(q1) * sin(q2) * sin(q3) * sin(q4) * d3 - sin(q1) * sin(q2) * cos(q4) * cos(q3) * d3 + cos(q1) * cos(q2) * cos(q3) * d2 - sin(q1) * sin(q2) * cos(q3) * d2 + cos(q1) * sin(q2) * d4 + cos(q1) * sin(q2) * d5 + cos(q2) * sin(q1) * d4 + cos(q2) * sin(q1) * d5;
X=[X0 X1 X2 X3 X4 X5 X6];
                           
Y0=0;
Y1=0;
Y2=0;
Y3=(cos(q1) * sin(q2) + sin(q1) * cos(q2)) * cos(q3) * (d3 + d2);
Y4=0.2e1 * cos(q1) * sin(q2) * cos(q3) ^ 2 * cos(q4) * d3 - 0.2e1 * cos(q1) * sin(q2) * cos(q3) * sin(q3) * sin(q4) * d3 + 0.2e1 * cos(q2) * sin(q1) * cos(q3) ^ 2 * cos(q4) * d3 - 0.2e1 * cos(q2) * sin(q1) * cos(q3) * sin(q3) * sin(q4) * d3 + 0.2e1 * cos(q1) * sin(q2) * cos(q3) ^ 2 * d2 + 0.2e1 * cos(q2) * sin(q1) * cos(q3) ^ 2 * d2 + cos(q1) * sin(q2) * cos(q3) * d2 - cos(q1) * sin(q2) * cos(q4) * d3 + cos(q2) * sin(q1) * cos(q3) * d2 - cos(q2) * sin(q1) * cos(q4) * d3 - cos(q1) * cos(q2) * d4 - cos(q1) * sin(q2) * d2 - cos(q2) * sin(q1) * d2 + sin(q1) * sin(q2) * d4;
Y5=cos(q1) * sin(q2) * cos(q3) * cos(q4) * d3 - cos(q1) * sin(q2) * sin(q3) * sin(q4) * d3 + cos(q2) * sin(q1) * cos(q3) * cos(q4) * d3 - cos(q2) * sin(q1) * sin(q3) * sin(q4) * d3 + cos(q1) * sin(q2) * cos(q3) * d2 + cos(q2) * sin(q1) * cos(q3) * d2 - cos(q1) * cos(q2) * d4 - cos(q1) * cos(q2) * d5 + sin(q1) * sin(q2) * d4 + sin(q1) * sin(q2) * d5;
Y6=-cos(q1) * sin(q2) * sin(q5) * sin(q3) * sin(q4) * d6 + cos(q1) * sin(q2) * sin(q5) * cos(q4) * cos(q3) * d6 + cos(q1) * sin(q2) * cos(q5) * sin(q3) * cos(q4) * d6 + cos(q1) * sin(q2) * cos(q5) * cos(q3) * sin(q4) * d6 - cos(q2) * sin(q1) * sin(q5) * sin(q3) * sin(q4) * d6 + cos(q2) * sin(q1) * sin(q5) * cos(q4) * cos(q3) * d6 + cos(q2) * sin(q1) * cos(q5) * sin(q3) * cos(q4) * d6 + cos(q2) * sin(q1) * cos(q5) * cos(q3) * sin(q4) * d6 - cos(q1) * sin(q2) * sin(q3) * sin(q4) * d3 + cos(q1) * sin(q2) * cos(q3) * cos(q4) * d3 - cos(q2) * sin(q1) * sin(q3) * sin(q4) * d3 + cos(q2) * sin(q1) * cos(q3) * cos(q4) * d3 + cos(q1) * sin(q2) * cos(q3) * d2 + cos(q2) * sin(q1) * cos(q3) * d2 - cos(q1) * cos(q2) * d4 - cos(q1) * cos(q2) * d5 + sin(q1) * sin(q2) * d4 + sin(q1) * sin(q2) * d5;
Y=[Y0 Y1 Y2 Y3 Y4 Y5 Y6];

Z0=0;
Z1=d1;
Z2=d1;
Z3=(cos(q1) * sin(q2) + sin(q1) * cos(q2)) * cos(q3) * (d3 + d2);
Z4=0.2e1 * cos(q3) ^ 2 * sin(q4) * d3 + 0.2e1 * sin(q3) * cos(q3) * d3 * cos(q4) + 0.2e1 * sin(q3) * d2 * cos(q3) + d2 * sin(q3) - d3 * sin(q4) + d1;
Z5=sin(q3) * d3 * cos(q4) + cos(q3) * d3 * sin(q4) + d2 * sin(q3) + d1;
Z6=sin(q5) * sin(q3) * cos(q4) * d6 + sin(q5) * cos(q3) * sin(q4) * d6 + cos(q5) * sin(q3) * sin(q4) * d6 - cos(q5) * cos(q4) * cos(q3) * d6 + sin(q3) * d3 * cos(q4) + cos(q3) * d3 * sin(q4) + d2 * sin(q3) + d1;
Z=[Z0 Z1 Z2 Z3 Z4 Z5 Z6];

% Chi ve quy dao diem thao tac
X1=[0 X6];
Y1=[0 Y6];
Z1=[0 Z6];
 %set(gca,'xlim',[-1.3 1.3],'Ylim',[-1.3 1.3],'Zlim',[0 1.3]);
plot3(X1,Y1,Z1,'b.')
refreshdata(Tool,'caller')
drawnow
grid on
 hold on


                        