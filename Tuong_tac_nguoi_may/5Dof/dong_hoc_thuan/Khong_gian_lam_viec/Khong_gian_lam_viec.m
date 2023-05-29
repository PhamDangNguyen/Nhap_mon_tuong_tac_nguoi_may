%%
clc
clear
close all
% Link length- can be changed  % length of first arm  % length of second arm % length of third arm
l1=0.56;
l2=0.42;
l3=0.24;
l4=0.37;
l5=0.47;
hold('on')
% Axis Properties
X=[0 0 l2 l2 l2 l2+l5];
Y=[0 0 0 0 0 0];
Z=[0 l1 l1 l1+l3 l1+l3+l4 l1+l3+l4];
Tool = plot3(X,Y,Z,'ro-','LineWidth',4,'XDataSource','X','YDataSource','Y','ZDataSource','Z');
axis([-2 2 -2 2 0 2]);
set(gca,'DataAspectRatio',[1 1 1])
grid on
hold('on')

xlabel('X(m)')
ylabel('Y(m)')
zlabel('Z(m)')

for q1 = -pi/2: 0.5 :pi/2
    for q2 = 0:0.3:l2
        for q3 =-pi/2:0.5:0
            for q4 =-pi/2:0.2:pi/2
                for q5 = 0:0.08:l5
                    % Ve quy dao cua 5 khau
                    X0=0;
                    X1=0;
                    X2=cos(q1) * q2;
                    X3=cos(q1) * (l3 * cos(q3) + q2);
                    X4=cos(q1) * (l3 * cos(q3) + cos(q3) * l4 + q2);
                    X5=-sin(q3) * cos(q4) * cos(q1) * q5 - sin(q1) * sin(q4) * q5 + cos(q1) * cos(q3) * l4 + cos(q1) * l3 * cos(q3) + cos(q1) * q2;
                    X=[X0 X1 X2 X3 X4 X5];
                    
                    Y0=0;
                    Y1=0;
                    Y2=sin(q1) * q2;
                    Y3=sin(q1) * (l3 * cos(q3) + q2);
                    Y4=sin(q1) * (l3 * cos(q3) + cos(q3) * l4 + q2);
                    Y5=-sin(q3) * sin(q1) * cos(q4) * q5 + sin(q4) * cos(q1) * q5 + sin(q1) * cos(q3) * l4 + sin(q1) * l3 * cos(q3) + sin(q1) * q2;
                    Y=[Y0 Y1 Y2 Y3 Y4 Y5];
                    
                    Z0=0;
                    Z1=l1;
                    Z2=l1;
                    Z3=-l3 * sin(q3) + l1;
                    Z4=-sin(q3) * l4 - l3 * sin(q3) + l1;
                    Z5=-cos(q3) * cos(q4) * q5 - sin(q3) * l4 - l3 * sin(q3) + l1;
                    Z=[Z0 Z1 Z2 Z3 Z4 Z5];
                    % Chi ve quy dao diem thao tac
                    X1=[0 X5];
                    Y1=[0 Y5];
                    Z1=[0 Z5];
                    %set(gca,'xlim',[-1.3 1.3],'Ylim',[-1.3 1.3],'Zlim',[0 1.3]);
                    plot3(X1,Y1,Z1,'b.')
                    refreshdata(Tool,'caller')
                    drawnow
                    grid on
                    hold on
                end
            end
        end
    end
end

