from _pylib import ffi, lib

def find(path):
    core = lib.mCoreFind(path.encode('UTF-8'))
    if core == ffi.NULL:
        return None
    return mCore(core)

class mCore:
    def __init__(self, native):
        self._core = ffi.gc(native, self._deinit)

    def init(self):
        success = bool(self._core.init(self._core))
        if success:
            if hasattr(self, 'PLATFORM_GBA') and self.platform() == self.PLATFORM_GBA:
                self.cpu = ARMCore(self._core.cpu)
                self.board = GBA(self._core.board)
            if hasattr(self, 'PLATFORM_GB') and self.platform() == self.PLATFORM_GB:
                self.cpu = LR35902Core(self._core.cpu)
                self.board = GB(self._core.board)
        return success

    def _deinit(self):
        self._core.deinit(self._core)

    def loadFile(self, path):
        return bool(lib.mCoreLoadFile(self._core, path.encode('UTF-8')))

    def autoloadSave(self):
        return bool(lib.mCoreAutoloadSave(self._core))

    def autoloadPatch(self):
        return bool(lib.mCoreAutoloadPatch(self._core))

    def platform(self):
        return self._core.platform(self._core)

    def desiredVideoDimensions(self):
        width = ffi.new("unsigned*")
        height = ffi.new("unsigned*")
        self._core.desiredVideoDimensions(self._core, width, height)
        return width[0], height[0]

    def reset(self):
        self._core.reset(self._core)

    def runFrame(self):
        self._core.runFrame(self._core)

    def runLoop(self):
        self._core.runLoop(self._core)

    def step(self):
        self._core.step(self._core)

if hasattr(lib, 'PLATFORM_GBA'):
    from .gba import GBA
    from .arm import ARMCore
    mCore.PLATFORM_GBA = lib.PLATFORM_GBA

if hasattr(lib, 'PLATFORM_GB'):
    from .gb import GB
    from .lr35902 import LR35902Core
    mCore.PLATFORM_GB = lib.PLATFORM_GB