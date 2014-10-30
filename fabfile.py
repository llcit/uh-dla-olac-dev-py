from fabric.api import local

def push_changes(message='fabfile committed this without comments.'):
    local("git add -A && git commit -m '%s'" % message)
    local("git push origin master")
