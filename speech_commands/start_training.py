import os
#os.system("ssh -i Hackathon2018-2.pem.txt ec2-user@18.191.114.207")
"""
Script used to put together all the flags for starting the training script in tensorflow
"""

#cmd  = "bazel run tensorflow/examples/speech_commands:train "

cmd  = "python train.py "
cmd += "--data_dir=/home/ec2-user/hackvie/data/processed "

# cmd += "--wanted_words=voices,threatening,satellites,bizarre,lurking,glowing,suspicious,"
# cmd += "delusion,withdraw,ringing,allegedly,meaning,implanting,chosen,deciphering,destiny,"
# cmd += "powers,patterns,strange,danger "

cmd += "--wanted_words=voices,danger,destiny "
#cmd += "implanting,satellites,powers,patterns,strange,suspicious,chosen "

cmd += "--sample_rate 1400 "
cmd += "--clip_duration_ms 2000 "
cmd += "--data_url '' "
cmd += "--background_volume .0001 "
cmd += "--background_frequency 0 "


if True:
    cmd += "--start_checkpoint=/home/ec2-user/hackvie/checkpoints/conv.ckpt-9000 "
else:
    # easy model to see if it would work
    cmd += "--model_architecture=single_fc "


#print(cmd)
os.system(cmd)
#os.system("scp -i Hackathon2018-2.pem.txt preprocess.py ec2-user@18.191.114.207:~/hackvie")