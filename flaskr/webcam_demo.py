import tensorflow as tf
import cv2
import time
from .posenet import load_model, read_cap, decode_multi, draw_skel_and_kp
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--model', type=int, default=101)
# parser.add_argument('--cam_id', type=int, default=0)
# parser.add_argument('--cam_width', type=int, default=1280)
# parser.add_argument('--cam_height', type=int, default=720)
# parser.add_argument('--scale_factor', type=float, default=0.7125)
# parser.add_argument('--file', type=str, default=None, help="Optionally use a video file instead of a live camera")
# args = parser.parse_args()

#Define the threshold variables for the given set
#bigtoepose
b_nose_x = 217.8
b_nose_y = 259.4
b_leftEye_x = 177.9
b_leftEye_x = 229
b_rightEye_x = 200.6
b_rightEye_y = 262.5
b_leftEar_x = 138.8
b_leftEar_y = 260.5
b_rightEar_x = 204.8
b_rightEar_y = 259.7
b_leftShoulder_x = 158.6
b_leftShoulder_y = 194.6
b_rightShoulder_x = 220.6
b_rightShoulder_y = 182.4
b_leftElbow_x = 155.8
b_leftElbow_y = 239
b_rightElbow_x = 233.4
b_rightElbow_y = 255
b_leftWrist_x = 155.8
b_leftWrist_y = 310.9
b_rightWrist_x = 178.3,
b_rightWrist_y = 349.7
b_leftHip_x = 237
b_leftHip_y = 45.6
b_rightHip_x = 266.8
b_rightHip_y = 62.5
b_leftKnee_x = 148.4
b_leftKnee_y = 203.1
b_rightKnee_x = 261.3
b_rightKnee_y = 218.5
b_leftAnkle_x = 247.7
b_leftAnkle_y = 370.4
b_rightAnkle_x = 195
b_rightAnkle_y = 363.3


#chairpose.jpg
c_nose_x = 315.9
c_nose_y = 118.8
c_leftEye_x = 311.1
c_leftEye_y = 111.2
c_rightEye_x = 315.9
c_rightEye_y = 110.7
c_leftEar_x = 311.1
c_leftEar_y = 111.7
c_rightEar_x = 302.4
c_rightEar_y = 104.2
c_leftShoulder_x = 298.4
c_leftShoulder_y = 123
c_rightShoulder_x = 282.2
c_rightShoulder_y = 108.8
c_leftElbow_x = 335.4
c_leftElow_y = 63.2
c_rightElbow_x = 312.7
c_rightElbow_y = 86.1
c_leftWrist_x = 353
c_leftWrist_y = 48.5
c_rightWrist_x = 336.4
c_rightWrist_y = 60.6
c_leftHip_x = 260
c_leftHip_y = 196.9
c_rightHip_x = 252.1
c_rightHip_y = 202.2
c_leftKnee_x = 318.7
c_leftKnee_y = 228.5
c_rightKnee_x = 325.8
c_rightKnee_y = 217.5
c_leftAnkle_x = 281.1
c_leftAnkle_y = 289.2
c_rightAnkle_x = 284.8
c_rightAnkle_y = 256.9


chair_pose_angle = math.acos(((c_rightAnkle_y-c_rightKnee_y)-(c_rightElbow_y-c_rightShoulder_y))/((c_rightAnkle_x - c_rightKnee_x)-(c_rightElbow_x - c_rightShoulder_x)))
big_toe_pose_angle = math.acos(((b_rightAnkle_y-b_rightKnee_y)-(b_rightElbow_y-b_rightShoulder_y))/((b_rightAnkle_x - b_rightKnee_x)-(b_rightElbow_x - b_rightShoulder_x)))


def webcam():
    with tf.Session() as sess:
        model_cfg, model_outputs = load_model(101, sess)
        output_stride = model_cfg['output_stride']

        # if args.file is not None:
        #     cap = cv2.VideoCapture(args.file)
        # else:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        start = time.time()
        frame_count = 0

        while True:
            input_image, display_image, output_scale = read_cap(
                cap, scale_factor=0.7125, output_stride=output_stride)

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )
            pose_scores, keypoint_scores, keypoint_coords = decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=1,
                min_pose_score=0.01)
            keypoint_coords *= output_scale

            # TODO this isn't particularly fast, use GL for drawing and display someday...
            overlay_image = draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.01, min_part_score=0.1)
             i = 0
            for pi in range(len(pose_scores)):
                if pose_scores[pi] == 0.:
                    break
                for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                    #print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
                    
                    #Checks for Sit Ups/Crunches
                    knee_joint = posenet.PART_NAMES[7] 
                    rightKnee_x = c[0]
                    rightKnee_y = c[1]

                    elbow_joint = posenet.PART_NAMES[13]
                    rightElbow_x = c[0]
                    rightElbow_y = c[1]
                    
                    shoulder_joint = posenet.PART_NAMES[6]
                    rightShoulder_x = c[0]
                    rightShoulder_y = c[1]
                    
                    ankle_joint = posenet.PART_NAMES[16]
                    rightAnkle_x = c[0]
                    rightAnkle_y = c[1]

                    #print("========================================")
                    #print(str(posenet.PART_NAMES[7])+' '+str(c[0]))
                    angle_knee_ankle_elbow_shoulder = math.acos((((rightAnkle_y-rightKnee_y)-(rightElbow_y-rightShoulder_y))/((rightAnkle_x - rightKnee_x)-(rightElbow_x - rightShoulder_x))))

            if (angle_knee_ankle_elbow_shoulder == chair_pose_angle):
                chair_pose_task = "done"
            else:
                chair_pose_task = "not completed"

            if (angle_knee_ankle_elbow_shoulder == big_toe_pose_angle):
                big_toe_pose_task = "done"
            else:
                big_toe_pose_task = "not completed"
            
            time_counter = time_counter+1

            #Adding helpful instructions for the user
            font = cv2.FONT_HERSHEY_SIMPLEX 
        
            # Use putText() method for 
            # inserting text on video 
            cv2.putText(overlay_image, 'Press Q when finised', (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_4)
            cv2.putText(overlay_image, 'Timer: '+str(time_counter), (50, 100), font, 1, (255, 0, 0), 2, cv2.LINE_4)
            cv2.putText(overlay_image, 'Big Toe Pose '+str(big_toe_pose_task), (50, 200), font, 1, (255, 0, 0), 2, cv2.LINE_4)
            cv2.putText(overlay_image, 'Chair Pose '+str(chair_pose_task), (50, 250), font, 1, (255, 0, 0), 2, cv2.LINE_4)
            

            cv2.imshow('posenet', overlay_image)
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print('Average FPS: ', frame_count / (time.time() - start))


if __name__ == "__main__":
    main()
