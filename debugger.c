#include <windows.h>
#ifdef __cplusplus__
extern "C" {
#endif
BOOL IsAttached() {
    return IsDebuggerPresent();
}
#ifdef __cplusplus__
}
#endif
