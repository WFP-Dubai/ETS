!define PRODUCT_NAME "ETS"
!define PRODUCT_DESCRIPTION "Electronic Tracking System"
!define PRODUCT_VERSION "0.0.3"
!define pkgdir "/home/werty/django_apps/ETS/windows/"
Var SYSTEMDRIVE

!include "MUI2.nsh"
!include "WriteEnvStr.nsh"
!include LogicLib.nsh
Name "${PRODUCT_NAME}"
Caption "Installation ${PRODUCT_NAME} - ${PRODUCT_DESCRIPTION} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}-${PRODUCT_VERSION}.exe" 
InstallDir ""
;RequestExecutionLevel admin

Function .onInit
  StrCpy $SYSTEMDRIVE $PROGRAMFILES 2
  StrCpy $INSTDIR "$SYSTEMDRIVE\ETS" 
FunctionEnd 

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

!define ReadEnvStr_RegKey \
     'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"' 


!define StrStr "!insertmacro StrStr"
 
!macro StrStr ResultVar String SubString
  Push `${String}`
  Push `${SubString}`
  Call StrStr
  Pop `${ResultVar}`
!macroend
 
Function StrStr
/*After this point:
  ------------------------------------------
  $R0 = SubString (input)
  $R1 = String (input)
  $R2 = SubStringLen (temp)
  $R3 = StrLen (temp)
  $R4 = StartCharPos (temp)
  $R5 = TempStr (temp)*/
 
  ;Get input from user
  Exch $R0
  Exch
  Exch $R1
  Push $R2
  Push $R3
  Push $R4
  Push $R5
 
  ;Get "String" and "SubString" length
  StrLen $R2 $R0
  StrLen $R3 $R1
  ;Start "StartCharPos" counter
  StrCpy $R4 0
 
  ;Loop until "SubString" is found or "String" reaches its end
  ${Do}
    ;Remove everything before and after the searched part ("TempStr")
    StrCpy $R5 $R1 $R2 $R4
 
    ;Compare "TempStr" with "SubString"
    ${IfThen} $R5 == $R0 ${|} ${ExitDo} ${|}
    ;If not "SubString", this could be "String"'s end
    ${IfThen} $R4 >= $R3 ${|} ${ExitDo} ${|}
    ;If not, continue the loop
    IntOp $R4 $R4 + 1
  ${Loop}
 
/*After this point:
  ------------------------------------------
  $R0 = ResultVar (output)*/
 
  ;Remove part before "SubString" on "String" (if there has one)
  StrCpy $R0 $R1 `` $R4
 
  ;Return output to user
  Pop $R5
  Pop $R4
  Pop $R3
  Pop $R2
  Pop $R1
  Exch $R0
FunctionEnd


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
  ${StrStr} $R1 $R0 '$INSTDIR\Python27\;$INSTDIR\Python27\Scripts'
  ${If} $R1 == ""
    StrCpy $R0 '$R0;$INSTDIR\Python27\;$INSTDIR\Python27\Scripts'
  ${EndIf}
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
  FileWrite $8 "explorer http://127.0.0.1:8000/$\r$\n"
  FileWrite $8 "python $\"$INSTDIR\ETS\bin\instance-script.py$\" runserver --insecure$\r$\n"
  FileClose $8
  AccessControl::GrantOnFile "$INSTDIR\ETS\db" "(BU)" "FullAccess + GenericRead + GenericWrite"
  FileOpen $9 $INSTDIR\ETS\import.bat w 
  FileWrite $9 "python $\"$INSTDIR\ETS\bin\instance-script.py$\" import_file -d $\"$DESKTOP\$\r$\n"
  FileClose $9
  CreateShortCut "$DESKTOP\ETS.lnk" "$INSTDIR\ETS\runserver.bat"
  CreateShortCut "$DESKTOP\import ETS data.lnk" "$INSTDIR\ETS\import.bat"  
  nsExec::Exec "python $\"$INSTDIR\ETS\bin\instance-script.py$\" import_file -d $\"$EXEDIR\"
;  ExecWait "$INSTDIR\ETS\import.bat" 
SectionEnd
