import time
import subprocess
import scrapper 
import alert
print("Preparing software.....".title())
bar_, a,b, c =scrapper.Get_barcode()



while c < len(bar_):
    try: 
        
        # Run the script
        process = subprocess.Popen(["python", "scrapper.py"])
        print("confirm")
    except Exception as e:
        # There was an error running the script, print the error and continue to the next iteration
        print(e)
        alert.send_alert1()
        continue
    except KeyboardInterrupt:
      print("you press close biutton")
      alert.send_alert1()

    # Wait for the script to finish
    process.wait()

    # Kill the script
    process.kill()
    delay = 3
    # Sleep for some time before running the script again
    print(f"will resart after {delay} seconds")
    time.sleep(delay)
alert.send_alert2()

