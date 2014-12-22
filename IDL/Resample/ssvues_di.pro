;PROGRAMME SSVUES_DI
;
;Octobre 2000
;
;
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; Extrait deux sous-vues en distance a partir d'une	image .ci2 		;
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
;
;********************************************************************
;* ENTREE: fichier image d'origine (.ci2)				   			*
;*		   nom du fichier image resultat(SANS extension !) 			*
;********************************************************************
;* SORTIE: sous-vue gauche (fichier image resultat + '_gch')		*
;*		   sous-vue droite (fichier image resultat + '_dte')		*
;*		   TF de l'image d'origine (fichier image resultat + '_fft')*
;*		   image d'origine en complexe (img_cplx)		   			*
;*		   affichage du spectre d'amplitude moyen decale   			*
;*         affichage du spectre d'amplitude moyen centre   			*
;********************************************************************
;
;


;LIGNE DE COMMANDE
;ssvues_di,'f1_0905_bat1.ci2','test'
;ssvues_di,'f1_0905_bat1b.ci2','test'




pro ssvues_di, racine, in_name, out_name

in_name=racine+'/'+in_name
out_name=racine+'/'+out_name
ouvfic, in_name, fid, nlig, ncol, dt, mi
close, fid
free_lun, fid
slc2cplx, in_name, nlig, ncol, image

;**********************************************
; Calcul de la TF par ligne de l'image complexe
;**********************************************

	tfimage = complexarr(ncol, nlig)
	tfimage = tfpar_lig(ncol, nlig, image)

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

	x=indgen(ncol)-ncol/2+1	;x = (fe-1)/(ncol-1)*indgen(ncol)-fe/2+1
	plot_names = ['Spec_di_moy - amplitude']
	!p.multi=0
	plot, x, tflig_ampl_moy, XRANGE=[min(x), max(x)], xstyle=1, title=plot_names

REPRISE: print,'Entrer la valeur du decalage'
		 read, dec
		 print, dec


;*********************************************************************************
; Multiplication de l'image d'origine par exp(-2*i*pi*dec*x) [centrage du spectre]
;*********************************************************************************
	if dec ne 0 then begin

		image_cen = complexarr(ncol,nlig)
		image_cen = mult_expo_lig(ncol, nlig, dec, image)


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

		x=indgen(ncol)-ncol/2+1
		;x = (fe-1)/(ncol-1)*indgen(ncol)-fe/2+1
		plot_names = ['Spec_di_moy_ampl centre']
		window,0
		plot, x, tflig_cen_ampl_moy, XRANGE=[min(x), max(x)], xstyle=1, title=plot_names
		;envi_plot_data, x, tflig_cen_ampl_moy
		print, 'Changer le decalage ? (0: non, 1: oui)'
		read, rep

		if rep eq 1 then begin
			goto, REPRISE
		endif
	endif else begin
		image_cen=image
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
	if (((size(w))(0) ne 0 ) and (w(0) ne 0 )) then begin		;
		tw=(size(w))[1]					; ensemble des ascisses connexe
		spec_cor(0:w(0)-1)=0.0			; plutot qu'un simple seuil
		spec_cor(w(tw-1):ncol-1)=0.0	;
	endif								;

	x=indgen(ncol)-ncol/2+1
	;x = (fe-1)/(ncol-1)*indgen(ncol)-fe/2+1
	plot_names = ['Spec_di_moy_ampl centre corrige']
	plot, x, spec_cor, XRANGE=[min(x), max(x)], xstyle=1, title=plot_names

	print, 'Changer la valeur de coef ? (0: non, 1: oui)'
	read, reponse

	if reponse eq 1 then begin

		goto, RETOUR

	endif


;*************************************************
; Decoupage en sous-vues en distance gauche/droite
;*************************************************
	sv_gauche = complexarr(ncol,nlig)
	sv_droite = complexarr(ncol,nlig)

	decoup_di, ncol, nlig, image_cen, tflig_cen_ampl_moy, sv_gauche, sv_droite, coef

	print, 'niveau moyens des sous vues et de l''image: ', mean(abs(sv_droite)), mean(abs(sv_gauche)), mean(abs(image))

;***********************************
; Conversion image complexe vers SLC
;***********************************
	sv_gauche_slc = intarr(ncol,nlig)
	sv_droite_slc = intarr(ncol,nlig)

	sv_gauche_slc = cplx2slc(ncol,nlig,sv_gauche)
	sv_droite_slc = cplx2slc(ncol,nlig,sv_droite)


;********************************************
; Creation des fichiers resultats (sous-vues)
;********************************************
	openw, unit, out_name+'_gch.ci2', /get_lun
	writeu, unit, sv_gauche_slc
	close, unit
	flush, unit

	com2 = ['Sous-vue gauche en distance de ',in_name]

	envi_setup_head, fname=out_name+'_gch', ns=ncol, nl=nlig, nb=2, $
		data_type=2, interleave=2, map_info=mi, /write, descrip=com2

	openw, unit, out_name+'_dte.ci2', /get_lun
	writeu, unit, sv_droite_slc
	close, unit
	flush, unit

	com3 = ['Sous-vue droite en distance de ',in_name]

	envi_setup_head, fname=out_name+'_dte', ns=ncol, nl=nlig, nb=2, $
		data_type=2, interleave=2, map_info=mi, /write, descrip=com3


;*****************************************
; Conversion image complexe vers amplitude
;*****************************************
	sv_dte_amp = intarr(ncol,nlig)
	sv_gch_amp = intarr(ncol,nlig)

	sv_dte_amp = fix(round(abs(sv_droite)))
	sv_gch_amp = fix(round(abs(sv_gauche)))

;********************************************
; Creation des fichiers resultats (sous-vues)
;********************************************
	openw, unit, out_name+'_dte_a.ui2', /get_lun
	writeu, unit, sv_dte_amp
	close, unit
	flush, unit
	free_lun, unit

	com2 = ['Sous-vue droite en distance de ',in_name]
	envi_setup_head, fname=out_name+'_dte_a', ns=ncol, nl=nlig, nb=1, $
		data_type=2, interleave=0, map_info=mi, /write, descrip=com2

	openw, unit, out_name+'_gch_a.ui2', /get_lun
	writeu, unit, sv_gch_amp
	close, unit
	flush, unit
	free_lun, unit
print, out_name

	com3 = ['Sous-vue gauche en distance de ',in_name]

	envi_setup_head, fname=out_name+'_gch_a', ns=ncol, nl=nlig, nb=1, $
		data_type=2, interleave=0, map_info=mi, /write, descrip=com3

	print,'FINI.'

end