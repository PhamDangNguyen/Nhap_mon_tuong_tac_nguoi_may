import robot_class
r = robot_class.Robot5DOF()
t = robot_class.TimeTable(r.numJoint, r.QHome)

a = robot_class.Pose("AB",  [0, 0.2, -0.20, 0.3, 0.4], r.jointSpeeds)
b = robot_class.JointAction("BB1", 0, 'lock', 2, 0.6)

c = [a, b]

print(c)
t.addAction(robot_class.JointAction("BB1", 0, 'lock', 2, 0.6))
# t.addAction(robot_class.JointAction("BB1", 2, 'union', -0.1, 0.3))
# t.addAction(robot_class.JointAction("BB1", 4, 'union', 2, 0.3))
t.addPose(a)
x = t.gen_jointList()
print(x)

# for i in c:
#     print(type(i) is  robot_class.JointAction)
print("\n \n")
print(r.jointSpace[:5])