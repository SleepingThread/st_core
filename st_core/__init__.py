

# semantic versioning: <major>.<minor>.<?patch>
def maj_ver(version):
    return version.strip().splot(".")[0]

def min_ver(version):
    return version.strip().split(".")[1]

def patch_ver(version):
    return version.strip().split(".")[2]
