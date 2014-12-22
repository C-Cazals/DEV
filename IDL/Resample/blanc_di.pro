;PROGRAMME FINE2STD_DI
;
;Octobre 2000
;
;
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; Extrait deux sous-vues en distance a partir d'une	image .ci2 		;
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;
;********************************************************************
;* ENTREE: matrice complexe d'origine 			   					*
;********************************************************************
;* SORTIE: image blanchie en distance (matrice complexe)			*
;*		   affichage du spectre d'amplitude moyen decale   			*
;*         affichage du spectre d'amplitude moyen centre   			*
;********************************************************************
;
;


pro blanc_di, matc_in, matc_out, nlig, ncol, fe

	tfimage = complexarr(ncol, nlig)
	tfimage = tfpar_lig(ncol, nlig, matc_in)

;*********************
; Passage en amplitude
;*********************
	tfimage_ampl = fltarr(ncol, nlig)
	tfimage_ampl = tab_cplx2mod_flt(tfimage)


;********************************************************
; Calcul et affichage du spectre d'amplitude moyen decale
;********************************************************
	tflig_ampl_moy = fltarr(ncol)
	tflig_ampl_moy = spec_ampl_di_moy_flt(ncol, nlig, tfimage_ampl)

	x = indgen(ncol)-ncol/2+1
	;x = (fe-1)/(ncol-1)*indgen(ncol)-fe/2+1
	plot_names = ['Spec_di_moy - amplitude']
	plot, x, tflig_ampl_moy, title=plot_names, xstyle=1, xrange=[min(x), max(x)]

REPRISE: print,'Entrer la valeur du decalage'
		 read, dec
		 print, dec


;*********************************************************************************
; Multiplication de l'image d'origine par exp(-2*i*pi*dec*x) [centrage du spectre]
;*********************************************************************************
	if dec ne 0 then begin
		image_cen = complexarr(ncol,nlig)
		image_cen = mult_expo_lig(ncol, nlig, dec, matc_in)


;***********************************************
; Calcul de la TF par colonne de l'image centree
;***********************************************
		tfimage_cen = complexarr(ncol, nlig)
		tfimage_cen = tfpar_lig(ncol, nlig, image_cen)

;*********************
; Passage en amplitude
;*********************
		tfimage_cen_ampl = fltarr(ncol, nlig)
		tfimage_cen_ampl = tab_cplx2mod_flt(tfimage_cen)


;********************************************************
; Calcul et affichage du spectre d'amplitude moyen centre
;********************************************************
		tflig_cen_ampl_moy = fltarr(ncol)
		tflig_cen_ampl_moy = spec_ampl_di_moy_flt(ncol, nlig, tfimage_cen_ampl)

		x = indgen(ncol)-ncol/2+1
		;x = (fe-1)/(ncol-1)*indgen(ncol)-fe/2+1
		window, 0
		plot_names = ['Spec_di_moy_ampl centre']
		plot, x, tflig_cen_ampl_moy, title=plot_names, xstyle=1, xrange=[min(x), max(x)]
		print, 'Changer le decalage ? (0: non, 1: oui)'
		read, rep

		if rep eq 1 then begin
			goto, REPRISE
		endif

	endif else begin
		image_cen=matc_in
		tfimage_cen=tfimage
		tfimage_cen_ampl=tfimage_ampl
		tflig_cen_ampl_moy=tflig_ampl_moy
	endelse


;************************************************************
; Determination du coefficient pour la mise a zero du spectre
;************************************************************
	print, 'Les valeurs du spectres inferieures a coef*min(spectre) seront mises a zero.'
RETOUR:	print, 'Valeur de coef ?'
		read, coef

	spec_cor = fltarr(ncol)
	spec_cor = tflig_cen_ampl_moy
	w=where(tflig_cen_ampl_moy gt coef*min(tflig_cen_ampl_moy))
	if (size(w))(0) ne 0 then begin		;
		tw=(size(w))[1]					; ensemble des ascisses connexe
		spec_cor(0:w(0)-1)=0.0			; plutot qu'un simple seuil
		spec_cor(w(tw-1):ncol-1)=0.0	;
	endif								;

	x = indgen(ncol)-ncol/2+1
	;x = (fe-1)/(ncol-1)*indgen(ncol)-fe/2+1
	plot_names = ['Spec_di_moy_ampl centre corrige']
	plot, x, spec_cor, title=plot_names, xstyle=1, xrange=[min(x), max(x)]

	print, 'Changer la valeur de coef ? (0: non, 1: oui)'
	read, reponse

	if reponse eq 1 then begin
		goto, RETOUR
	endif

;*************************************************
; Decoupage en sous-vues en distance gauche/droite
;*************************************************
	matc_out = complexarr(ncol,nlig)

	for i = 0, nlig-1 do begin
		ligne = image_cen(0:ncol-1,i)
		spectre = fft(ligne)
		spectre(0:w(0)-1)=0.0
		spectre(w(tw-1):ncol-1)=0.0
		spec_nrj = (spectre/tflig_cen_ampl_moy)*(sqrt(mean((abs(spectre))^2)))
		matc_out(0:ncol-1,i) = fft(spec_nrj,1)
	endfor


end