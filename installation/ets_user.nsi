!define PRODUCT_NAME "ETS"
!define PRODUCT_DESCRIPTION "Electronic Tracking System"
!define PRODUCT_VERSION "0.0.1"
!define pkgdir "/home/werty/django_apps/ETS/windows/"

!include "MUI2.nsh"
!include "WriteEnvStr.nsh"
Name "${PRODUCT_NAME}"
Caption "Installation ${PRODUCT_NAME} - ${PRODUCT_DESCRIPTION} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}-${PRODUCT_VERSION}.exe" 
;RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\ETS"

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

!define ReadEnvStr_RegKey \
     'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"' 

InstType "Auto"
InstType "Manual"

SectionGroup /e "Requirements"

Section #
  SectionIn 1 2 RO
  ReadEnvStr $R0 "PATH"  
SectionEnd

SectionGroup "Python"
Section "Auto" SecPythonAuto
  SectionIn 1
  SetOutPath "$TEMP"
  File "${pkgdir}\python-2.7.2.msi"
  ExecWait "msiexec.exe /i $\"$TEMP\python-2.7.2.msi$\" /qn TARGETDIR=$\"$INSTDIR\Python27$\""
  Delete "$TEMP\python-2.7.2.msi" 
  StrCpy $R0 '$R0;$INSTDIR\Python27\;$INSTDIR\Python27\Scripts'
SectionEnd

Section "Manual" SecPythonManual
  SectionIn 2
  SetOutPath "$TEMP"
  File "${pkgdir}\python-2.7.2.msi"
  ExecWait "msiexec.exe /i $\"$TEMP\python-2.7.2.msi$\" /qb"
  Delete "$TEMP\python-2.7.2.msi" 
SectionEnd
SectionGroupEnd

Section "PIL" SecPIL
  SectionIn 1 2
  SetOutPath "$TEMP"
  File "${pkgdir}\PIL-1.1.7.win32-py2.7.exe"
  ExecWait "$TEMP\PIL-1.1.7.win32-py2.7.exe"
  Delete "$TEMP\PIL-1.1.7.win32-py2.7.exe"
SectionEnd

Section #
  SectionIn 1 2 RO
  Push PATH
  Push '$R0'	
  Call WriteEnvStr
SectionEnd

SectionGroupEnd

Section "Main" MainProgram
  SectionIn 1 2
  SetOutPath "$INSTDIR\ETS"
  File /r "${pkgdir}\ETS\*"
  FileOpen $8 $INSTDIR\ETS\runserver.bat w 
  FileWrite $8 "python $\"$INSTDIR\ETS\bin\instance-script.py$\" runserver --insecure"
  FileClose $8
  CreateShortCut "$DESKTOP\ETS.lnk" "$INSTDIR\ETS\runserver.bat" 
SectionEnd

 
Function .onSelChange

  !insertmacro StartRadioButtons $1
    !insertmacro RadioButton ${SecPythonAuto}
    !insertmacro RadioButton ${SecPythonManual}
  !insertmacro EndRadioButtons

FunctionEnd 