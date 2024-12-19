#
# Here we create AI Model which will act as Wendy Addams
# 
# Wednesday is an American Gothic coming-of-age supernatural mystery comedy 
# thriller television series based on the character Wednesday Addams 
# by Charles Addams.
#
https://github.com/ollama/ollama/blob/main/docs/modelfile.md

I do use llama3.2:3b image. You can read about it here:
https://ollama.com/library/llama3.2 

#if you do not have it, you can pull it:
ollama pull llama3.2:3b

#run this command to create Wendy Addams
#by using existing model file

ollama create wednesday --file wednesday

#This command will give you modefile
#for the any model you have already
#This is not required for the project, just to
#satisfy your curiocity

ollama show <model> --modelfile > modelfile

