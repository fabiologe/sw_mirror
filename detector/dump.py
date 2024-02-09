if person_inside:
            #text = "Person"
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            cv2.imwrite("jpgs/person_detected_{}.jpg".format(timestamp), frame)
            if not timer_started:
                start_time = time.time()
                timer_started = True

        if timer_started:
            current_time = time.time()
            if current_time - start_time > 180:  # 3 minutes in seconds
                delete_old_images()
