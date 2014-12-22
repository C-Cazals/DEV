
pro ouvfic, in_name, fid, nlig, ncol, dt, mi, xs, ys, bn, nb

;*******************************************
; Lecture des parametres du fichier image
;*******************************************
	point=-1
	ouv=1
	fids = envi_get_file_ids()

	if (fids(0) ne -1) then begin
		for i=0, n_elements(fids)-1 do begin
 			 envi_file_query, fids(i), fname=fname
 			 if strmid(fname,1) eq strmid(in_name,1) then begin
 			 	point=i
  			 	print, i, ':	', fname
  			 endif
		endfor
		if point ge 0 then	begin
			fid=fids(point)
			ouv=0
		endif
	endif
	if ouv eq 1 then begin
		envi_open_file, in_name, r_fid=fid
		if (fid eq -1) then begin
			print, 'erreur d''ouverture'
			return
		endif
	endif
	mi=envi_get_map_info(fid=fid)
	envi_file_query, fid, nl = nlig, ns = ncol, data_type=dt, $
			xstart=xs, ystart=ys, bnames=bn, nb=nb
	envi_file_mng, id=fid, /remove
end