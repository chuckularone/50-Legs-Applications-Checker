import subprocess

# The command you want to execute
command = "curl -X POST https://maker.ifttt.com/trigger/50Legs/with/key/f4Lwi-yUBJL1cH1u0ocWrSrEaz9OFYBvBFrc5mtm0Jl"

# Execute the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Get the output and error (if any)
output, error = process.communicate()

# Print the output and error
print("Output:", output.decode())
print("Error:", error.decode())
