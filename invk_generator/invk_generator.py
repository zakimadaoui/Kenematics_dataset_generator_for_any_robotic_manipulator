import numpy as np
import math
from data_parser import loadData

def c(t):
        return math.cos(math.radians(t))

def s(t):
        return math.sin(math.radians(t))


def generate_angles(num_dofs):
    angles = np.random.uniform(low = -360, high = 360, size = (num_dofs,))
    return angles


#TODO find the right implementation  of getting the rotation angles
def getRotations(r):

        roll = math.atan2(r[2][1],r[2][2])
        pitch = math.atan2(r[1][0],r[0][0])

        if math.cos(pitch) == 0:
                yaw = math.atan2(-r[2][0],r[1][0]/math.sin(r))
        else:
                yaw = math.atan2(-r[2][0],r[1][0]/math.cos(pitch))

        return roll,pitch,yaw
        #return math.degrees(roll),math.degrees(pitch),math.degrees(yaw)



def getTransformation(dh):

        T0_3 = np.array(
                [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])

        Temp = []
        l = len(dh) // 4

        for i in range(1, (l + 1)):
                t = dh["t" + str(i)]
                q = dh["q" + str(i)]
                d = dh["d" + str(i)]
                a = dh["a" + str(i)]

                Temp = np.array(
                        [[c(t), -s(t) * c(q), s(t) * s(q), a * c(t)],
                         [s(t), c(t) * c(q), -c(t) * s(q), a * s(t)],
                         [0, s(q), c(q), d],
                         [0, 0, 0, 1]])

                T0_3 = T0_3 @ Temp

        x = T0_3[0][3]
        y = T0_3[1][3]
        z = T0_3[2][3]

        roll, pitch, yaw = getRotations(T0_3)

        # print("x = " + str(x))
        # print("y = " + str(y))
        # print("z = " + str(z))
        #
        # print("\nT matrix: \n")
        #
        # print(T0_3)


        return x,y,z,roll,pitch,yaw


# generates one example inputs and outputs to files : inputs.txt / outputs.txt
def generate_inputs_and_outputs(dh_params):

    x, y, z, roll, pitch, yaw = getTransformation(dh_params)
    inputs = str(x) + "," + str(y) + "," + str(z) + "," + str(roll) + "," + str(pitch) + "," + str(yaw) + "\n"
    outputs = str(joint_angles[0]) + "," + str(joint_angles[1]) + "," + str(joint_angles[2]) + "\n"

    with open("inputs.txt", 'a') as in_file:
        in_file.write(inputs)

    with open("outputs.txt", 'a') as out_file:
        out_file.write(outputs)


 # ==================================================== Main =========================================================

#erasing files contents
with open("inputs.txt",'w') as i:
    i.write("")

with open("outputs.txt",'w') as o:
    o.write("")


#lines lengths
l = [7,7,9]
#number of rotating joints
num_dofs = 3

num_examples = 10000

print("generating data ..... ")

for i in range(num_examples):
    # randomly generated joint angles for one example
    joint_angles = generate_angles(num_dofs)

    # DH parameters
    dh_params = {"q1": 90, "a1": 0, "d1": l[0], "t1": joint_angles[0],
          "q2": 0, "a2": l[1], "d2": 0, "t2": joint_angles[1],
          "q3": 0, "a3": l[2], "d3": 0, "t3": -joint_angles[2]
          }

    generate_inputs_and_outputs(dh_params)

print("Done generating data ! ")

# load and print data :
X,Y = loadData("inputs.txt","outputs.txt")
print("inputs: ")
print(X.shape)
# print(X)

print("\noutputs: ")
print(Y.shape)
# print(Y)
