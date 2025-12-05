# Make app directory
mkdir app

# Move the main file into it
git mv chatbot_ui.py app/chatbot_ui.py

# If there are other support files, move them appropriately
# e.g. git mv my_file.txt app/my_file.txt   (or delete it if not needed)

# Commit changes
git commit -m "Reorganize folder structure: move main app into app/"

# Push
git push origin main
