!define PRODUCT_NAME "ETS"
!define PRODUCT_DESCRIPTION "Electronic Tracking System"
!define PRODUCT_VERSION "0.0.1"
!define pkgdir "/home/werty/django_apps/ETS/windows/"

!include "MUI2.nsh"
!include "WriteEnvStr.nsh"
Name "${PRODUCT_NAME}"
Caption "Installation ${PRODUCT_NAME} - ${PRODUCT_DESCRIPTION} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}-${PRODUCT_VERSION}.exe" 
InstallDir "$PROGRAMFILES\ETS"
;SetCompressor lzma

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

;!insertmacro MUI_UNPAGE_WELCOME
;!insertmacro MUI_UNPAGE_CONFIRM
;!insertmacro MUI_UNPAGE_INSTFILES

;  WriteRegStr HKEY_LOCAL_MACHINE "Software\Microsoft\Windows\CurrentVersion\Run" "Notepad" "$WinDir\Notepad.exe"
;  MessageBox MB_OK|MB_ICONINFORMATION "Блокнот теперь будет запускаться вместе с Windows"

!define ReadEnvStr_RegKey \
     'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"' 

InstType "Auto"
InstType "Manual"
InstType "Auto (ETS from Internet)"
InstType "Manual (ETS from Internet)"

SectionGroup /e "Requirements"

Section #
  SectionIn 1 2 3 4 RO
  ReadEnvStr $R0 "PATH"  
  messagebox mb_ok '$R0'
SectionEnd

SectionGroup "Python"
Section "Auto" SecPythonAuto
  SectionIn 1 3
  SetOutPath "$TEMP"
  File "${pkgdir}\python-2.7.2.msi"
  ExecWait "msiexec.exe /i $\"$TEMP\python-2.7.2.msi$\" /qn TARGETDIR=$\"$INSTDIR\Python27$\""
  Delete "$TEMP\python-2.7.2.msi" 
  StrCpy $R0 '$R0;$INSTDIR\Python27\;$INSTDIR\Python27\Scripts'
SectionEnd

Section "Custom" SecPythonCustom
  SectionIn 2 4
  SetOutPath "$TEMP"
  File "${pkgdir}\python-2.7.2.msi"
  ExecWait "msiexec.exe /i $\"$TEMP\python-2.7.2.msi$\" /qb"
  Delete "$TEMP\python-2.7.2.msi" 
SectionEnd
SectionGroupEnd


;  ReadEnvStr $R0 "PATH"
;  messagebox mb_ok '$R0'
;  StrCpy $R0 "$R0;C:\Python27\;C:\Python27\Scripts"
;  System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("PATH", R0).r2'
;  ReadEnvStr $R0 "PATH"
;  messagebox mb_ok '$R0'

;  !define ReadEnvStr_RegKey 'HKCU "Environment"'
  


;  Push '$R0;C:\Python27\;C:\Python27\Scripts'	

;  !define ReadEnvStr_RegKey 'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"'
;  ReadEnvStr $R0 "PATH"
;  Push PATH
;  Push '$R0;C:\Python27\;C:\Python27\Scripts'
;  Call WriteEnvStr


Section "Pywin" SecPyWin
  SetOutPath "$TEMP"
  File "${pkgdir}\pywin32-216.win32-py2.7.exe"
  ExecWait "$TEMP\pywin32-216.win32-py2.7.exe"
  Delete "$TEMP\pywin32-216.win32-py2.7.exe"
SectionEnd

SectionGroup "MinGW"
Section "Auto" SecMinGWAuto
  SectionIn 1 3
  SetOutPath "$TEMP"
  File "${pkgdir}\mingw-get-inst-20110802.exe"
  ExecWait "$TEMP\mingw-get-inst-20110802.exe /verysilent /sp- /dir=$\"$INSTDIR\MinGW$\""
  Delete "$TEMP\mingw-get-inst-20110802.exe"
  StrCpy $R0 '$R0;$INSTDIR\MinGW\bin'	
  FileOpen $9 $INSTDIR\Python27\Lib\distutils\distutils.cfg w 
  FileWrite $9 "[build]$\r$\n"
  FileWrite $9 "compiler=mingw32$\r$\n"
  FileClose $9
SectionEnd

Section "Custom" SecMinGWCustom
  SectionIn 2 4
  SetOutPath "$TEMP"
  File "${pkgdir}\mingw-get-inst-20110802.exe"
  ExecWait "$TEMP\mingw-get-inst-20110802.exe"
  Delete "$TEMP\mingw-get-inst-20110802.exe"
SectionEnd
SectionGroupEnd

Section "PIL" SecPIL
  SetOutPath "$TEMP"
  File "${pkgdir}\PIL-1.1.7.win32-py2.7.exe"
  ExecWait "$TEMP\PIL-1.1.7.win32-py2.7.exe"
  Delete "$TEMP\PIL-1.1.7.win32-py2.7.exe"
SectionEnd

SectionGroup "Git"
Section "Auto" SecGitAuto
  SectionIn 3
  SetOutPath "$TEMP"
  File "${pkgdir}\Git-1.7.4-preview20110204.exe"
  ExecWait "$TEMP\Git-1.7.4-preview20110204.exe /verysilent /sp- /dir=$\"$INSTDIR\Git$\""
  Delete "$TEMP\Git-1.7.4-preview20110204.exe"
  StrCpy $R0 '$R0;$INSTDIR\Git\cmd\'	
SectionEnd

Section "Custom" SecGitCustom
  SectionIn 4
  SetOutPath "$TEMP"
  File "${pkgdir}\Git-1.7.4-preview20110204.exe"
  ExecWait "$TEMP\Git-1.7.4-preview20110204.exe"
  Delete "$TEMP\Git-1.7.4-preview20110204.exe"
SectionEnd
SectionGroupEnd

SectionGroup "Subversion client"
Section "Auto" SecSubversionAuto
  SectionIn 3
  SetOutPath "$TEMP"
  File "${pkgdir}\CollabNetSubversion-client-1.7.1-1-Win32.exe"
  ExecWait "$TEMP\CollabNetSubversion-client-1.7.1-1-Win32.exe /S /D=$\"$INSTDIR\Subversion Client$\""
  Delete "$TEMP\CollabNetSubversion-client-1.7.1-1-Win32.exe"
SectionEnd

Section "Custom" SecSubversionCustom
  SectionIn 4
  SetOutPath "$TEMP"
  File "${pkgdir}\CollabNetSubversion-client-1.7.1-1-Win32.exe"
  ExecWait "$TEMP\CollabNetSubversion-client-1.7.1-1-Win32.exe"
  Delete "$TEMP\CollabNetSubversion-client-1.7.1-1-Win32.exe"
SectionEnd
SectionGroupEnd

Section #
  SectionIn 1 2 3 4 RO
  messagebox mb_ok '$R0'
  Push PATH
  Push '$R0'	
  Call WriteEnvStr
SectionEnd

SectionGroupEnd


SectionGroup "ETS"
Section "Main" MainProgram
  SectionIn 1 2
  SetOutPath "$INSTDIR\ETS"
;  File /r "${pkgdir}\ETS\*"
SectionEnd
 
Section "From Internet" MainProgramInternet
  SectionIn 3 4
;  nsExec::Exec "git clone https://github.com/WFP-Dubai/ETS.git $INSTDIR"
;  nsExec::Exec "python $INSTDIR\bootstrap.py"
;  nsExec::Exec "$INSTDIR\bin\buildout -c $INSTDIR\windows.cfg"
SectionEnd
SectionGroupEnd

;Function .onSelChange

;  !insertmacro StartRadioButtons $1
;    !insertmacro RadioButton ${SecPythonAuto}
;    !insertmacro RadioButton ${SecPythonCustom}
;  !insertmacro EndRadioButtons

;  !insertmacro StartRadioButtons $2
;    !insertmacro RadioButton ${SecMinGWAuto}
;    !insertmacro RadioButton ${SecMinGWCustom}
;  !insertmacro EndRadioButtons

;  !insertmacro StartRadioButtons $3
;    !insertmacro RadioButton ${SecGitAuto}
;    !insertmacro RadioButton ${SecGitCustom}
;  !insertmacro EndRadioButtons

;  !insertmacro StartRadioButtons $4
;    !insertmacro RadioButton ${SecSubversionAuto}
;    !insertmacro RadioButton ${SecSubversionCustom}
;  !insertmacro EndRadioButtons

;  !insertmacro StartRadioButtons $5
;    !insertmacro RadioButton ${MainProgram}
;    !insertmacro RadioButton ${MainProgramInternet}
;  !insertmacro EndRadioButtons

;FunctionEnd 
