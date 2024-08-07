import ctypes
from ctypes import wintypes
import psutil

# Define constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

# Define MEMORY_BASIC_INFORMATION structure
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", wintypes.LPVOID),
        ("AllocationBase", wintypes.LPVOID),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD)
    ]

# Define Windows API functions
kernel32 = ctypes.WinDLL('kernel32')
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

VirtualQueryEx = kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]
VirtualQueryEx.restype = ctypes.c_size_t

ReadProcessMemory = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
ReadProcessMemory.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

def get_memory_bytes(process_id):
    try:
        # Check if the process exists
        process = psutil.Process(process_id)
    except psutil.NoSuchProcess:
        raise Exception(f"Process with ID {process_id} does not exist.")
    except psutil.AccessDenied:
        raise Exception(f"Access denied to process with ID {process_id}.")
    
    # Open the process
    process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, process_id)
    if not process_handle:
        raise Exception("Could not open process")

    memory_bytes = bytearray()
    address = 0

    while True:
        mbi = MEMORY_BASIC_INFORMATION()
        result = VirtualQueryEx(process_handle, address, ctypes.byref(mbi), ctypes.sizeof(mbi))
        if result == 0:
            break
        
        # Check if the memory region is readable
        if mbi.Protect & (PAGE_READONLY | PAGE_READWRITE | PAGE_EXECUTE_READ | PAGE_EXECUTE_READWRITE):
            region_size = mbi.RegionSize
            if region_size > 0:
                buffer = ctypes.create_string_buffer(region_size)
                bytes_read = ctypes.c_size_t()
                if ReadProcessMemory(process_handle, address, buffer, region_size, ctypes.byref(bytes_read)):
                    memory_bytes.extend(buffer.raw[:bytes_read.value])
        
        # Move to the next memory region
        address += mbi.RegionSize

    # Close the handle to the process
    CloseHandle(process_handle)
    
    return memory_bytes

# Define protection constants
PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READ = 0x20
PAGE_EXECUTE_READWRITE = 0x40