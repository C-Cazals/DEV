pro svm_greedy_forward_bin

  COMMON SHARE , ns,nl,nb,nb_classif,best_c, best_g
  COMMON SHARE2 ,CV , svm_train_path, gnuplot_path

  full_greedy =1; Greedy from 0 input feature/1greedy from 1 input feature 0

  best_c = 1024.
  best_g = 1

  pas=1; Nombre de primitives ajoutées à chaque itération
  pas_cv = 1;pas de cv

  CV = 0; Valeur par defaut de la CV (désactivée)

  svm_train_path = 'svm-train-bin'
  if !VERSION.OS_FAMILY eq 'unix' then begin
	gnuplot_path = 'gnuplot'
endif else begin
	gnuplot_path = 'C:\gnuplot\bin\pgnuplot'
endelse

  name_file = envi_pickfile(title='Selectionner le fichier source de classification')
  if (name_file eq '') then return
  directory = FILE_DIRNAME(name_file,/mark_directory) ;On stocke la directory du fichier source

  envi_open_file, name_file, r_fid=fid ;On ouvre le fichier selectionner
  if (fid eq -1) then return

  ENVI_SELECT, fid=fid,dims=dims,pos=pos, $ ;On selectionne les bandes du fichier a classifier
  file_type=ftype, $
  title='Selectionner le fichier ainsi que les bandes de départ a utiliser pour la classification'
  if (fid[0] eq -1) then return

  envi_file_query, fid, ns=ns, nl=nl, nb=nb,bnames=bnames,dims=dims

filesortieroiT=directory+'imgroi.t';Chemin du fichier de sortie du ROI
filesortieroiC=directory+'imgroi.c' ; Chemin du fichier de sortie Image au format LIBSVM

  fileroiT = envi_pickfile(title='Selectionner le fichier roi d_entrainement', filter='*.roi')
    if (fileroiT eq '') then return
  fileroiC=DIALOG_PICKFILE(PATH=directory, filter='*.roi', /READ, Title='Entrez le fichier ROI de control');Chemin du fichier
    if (fileroiC eq '') then return


  fileclassement=directory+'classement_iter.txt'
  tab_band= pos

  tab_img=indgen(nb); tableau des numero de bande de l'image enti�re

Openw, unit_rank, directory+'rank_final.txt', /GET_LUN
  printf,unit_rank,'#############################################'
  printf,unit_rank,'Classement SIMPLIFIE des primitives'
  printf,unit_rank,'#############################################'
printf,unit_rank, bnames[tab_band]

  Openw, unitclassement, fileclassement, /GET_LUN
  printf,unitclassement,'#############################################'
  printf,unitclassement,'Classement des primitives par itération successive et basée sur le MPA'
  printf,unitclassement,'#############################################'
  printf,unitclassement,''
  nb_temp=n_elements(pos);nombre de bande de la boucle while
  if (full_greedy eq 1) then nb_temp = 0

 ; print,'Tab_band avant le while',tab_band

  count_step_it = 0
  While nb_temp lt nb do begin
;    print,'boucle while nb_temp =',nb_temp
;    print,'Tab_band debut du while',tab_band

;    if count_step_it eq pas_cv then begin
;      cv =1
;      count_step_it = 0
;    endif
    if (full_greedy eq 1 and count_step_it eq 0) then begin
      tab_band_sup=lindgen(nb)
      nb_iter = nb
      sz_ = 0
    endif else begin
      sz=size(tab_band)
      sz_=sz[1]
      nb_iter=nb-sz_
      tab_band_sup=lonarr(nb_iter)
      temp_iter=0
      for i=0,nb-1 do begin
        wh=where(tab_band EQ tab_img[i], count)
        print, i, count
        if (count eq 0) then begin
          tab_band_sup[temp_iter]=tab_img[i] & temp_iter=temp_iter+1
       endif
      endfor
    endelse
    stats_iter=fltarr(nb_iter)
 ;   im_temp=fltarr(ns,nl,sz_+1)
    stat_iter=fltarr(nb_iter)

    fileclassement_temp=directory+'classement_nbEQ_'+strn(nb_temp)+'_.txt'
    Openw, unitclassement_temp, fileclassement_temp, /GET_LUN

    printf,unitclassement,''
    printf,unitclassement,'-------------Nombre de bandes--actuelles',nb_temp
    printf,unitclassement,'Parametre rbf : C= ',string(best_c),' G= ',string(best_g)
    printf,unitclassement,''

    printf,unitclassement_temp,''
    printf,unitclassement_temp,'-------------Nombre de bande--actuel',nb_temp
  printf,unitclassement_temp,'Parametre rbf : C= ',string(best_c),' G= ',string(best_g)

  if (full_greedy eq 1 and count_step_it eq 0) then begin
  printf,unitclassement,'Bande actelles : Aucune'
  endif else begin
    printf,unitclassement,'Bande actelles : '
    printf,unitclassement,bnames[tab_band]
  endelse


    For i=0,nb_iter-1 do begin;Boucle pour tester toute les primitives restantes
  ;    print, 'i eme iteration :',i
      if (full_greedy eq 1 and count_step_it eq 0) then begin
        ;tab_band = tab_band_sup
        comb_ = tab_band[i]
      endif else begin
        comb_=lonarr(sz_+1)
        comb_[0:sz_-1]=tab_band & comb_[sz_]=tab_band_sup[i];On creer un tableau contenant les bandes de la ième itération
      endelse
  ;    print,'ensemble des bande de la ième iteration ',comb_

    nb_classif = sz_+1

      svm_classified,name_file,directory,fileroiT,fileroiC,fid,comb_,classif_name_out; génération de la ième classif
      cv =0

      classif_name_out = directory + 'classif_svm_tmp'

      stat_iter[i]=stats_classif_gen(classif_name_out ,classif_name_out+'_iter_'+strn(nb_iter)+'_bande_'+strn(i),fileroiC);génération du mpa

      printf,unitclassement,format='(A12,A20,A7,A7)','Primitive teste : ',bnames[tab_band_sup[i]],' Mpa= ',strn(100.*stat_iter[i],length=7)
      printf,unitclassement_temp,format='(A12,A20,A7,A7)','Primitive ajoutee : ',bnames[tab_band_sup[i]],' Mpa= ',strn(100.*stat_iter[i],length=7)
    endfor
    max_mpa_iter=max(stat_iter)
    sort_mpa=sort(stat_iter)
    for i=nb_iter-pas,nb_iter-1 do begin
      printf,unitclassement,'Primitive ajoute : '
      printf,unitclassement,format='(A20,A7,A7)',bnames[tab_band_sup[sort_mpa(i)]],' Mpa= ',strn(100.*stat_iter[sort_mpa(i)],length=7)

      printf,unitclassement_temp,'Primitive ajoute : '
      printf,unitclassement_temp,format='(A20,A7,A7)',bnames[tab_band_sup[sort_mpa(i)]],' Mpa= ',strn(100.*stat_iter[sort_mpa(i)],length=7)

      printf,unit_rank,format='(A6,A20,A7,A5,A4,A7,A4,A10)','P_add ',bnames[tab_band_sup[sort_mpa(i)]],' ',strn(100.*stat_iter[sort_mpa(i)],length=4), ' C= ',strn(best_c,length=7),' G= ',strn(best_g,length=10)
      ;printf,unit_rank,format='(A6,A20,A7,A4,A7,A4,A10)','P_add ',bnames[tab_band_sup[sort_mpa(i)]],' ',strn(100.*stat_iter[sort_mpa(i)],length=6), ' C= ',strn(best_c,length=7),' G= ',strn(best_g,length=10)
    endfor
    free_lun,unitclassement_temp

  ;  print,'stat en fin de boucle for :'

    tab_band_temp=tab_band
    tab_band=intarr(sz_+pas)
    if (full_greedy eq 1 and count_step_it eq 0) then begin
      tab_band[sz_:sz_+pas-1]=tab_band_sup[sort_mpa[nb_iter-pas:nb_iter-1]]
    endif else begin
      tab_band[0:sz_-1]=tab_band_temp & tab_band[sz_:sz_+pas-1]=tab_band_sup[sort_mpa[nb_iter-pas:nb_iter-1]]
    endelse

;    print,'Tab_band fin du while',tab_band
    nb_temp=nb_temp+pas


    count_step_it = count_step_it + 1
  endwhile
free_lun,unit_rank
free_lun,unitclassement
end

pro svm_classified,name_file,directory,fileroiT,fileroiC,fid,pos,filetemp
COMMON SHARE
COMMON SHARE2
  envi_delete_rois, /ALL
  ENVI_RESTORE_ROIS,fileroiT
  roi_ids = envi_get_roi_ids(ROI_COLORS=roi_colors,ROI_NAMES=roi_names,fid=fid,/SHORT_NAME); On stocke les infos des classes (couleur, noms...)

  nbroi_=size(roi_ids,/dimensions)
  nbroi=nbroi_[0]

  class_names = strarr(nbroi+1)
  class_names[0] = 'unclassified' & class_names[1:nbroi] = roi_names

  lookup = bytarr(3,nbroi+1)
  lookup[*,0] = [0,0,0] & lookup[*,1:nbroi] = roi_colors

  file_roiT_to_libsvm = directory + 'training.bin' ;Nom du fichier d_entrainement de sortie au format libsvm
  roi_to_libsvm_bin, file_roiT_to_libsvm, fid, pos ; On creer le fichier binaire d'entrainement

  file_addr_mask = directory + 'addr.bin'

  envi_delete_rois, /ALL
  ENVI_RESTORE_ROIS,fileroiC

  addr_to_bin, file_addr_mask, fid, 0,1,pos ; On creer le fichier binaire contenant les adresses des pixel à classer (contrôle)

;;;;;;;;;;;;;;;;Classification
  fileout = directory + 'classif_svm_tmp'
  svm_param=script_svm(directory,'script_svm.bat',fileout, name_file, file_addr_mask)

;;;;;;;;;;;;Conversion du fichier de sortie libsvm en fichier de classif
envi_setup_head, fname=fileout, ns=ns, nl=nl, interleave=0, data_type=4, nb=1,NUM_CLASSES=nbroi+1, $
CLASS_NAMES=class_names, $
file_type = envi_file_type('ENVI Classification'),$
lookup = lookup,$
/write, /open

end
pro roi_to_libsvm_bin,fileout,fid, pos; Fonction qui convertie le roi d'une image au format libsvm
  envi_file_query, fid, dims=dims, ns=ns, nl=nl ;On recupere les informations de taille de l_image
;  sz_im = SIZE(pos)
;  nb=sz_im[1]
  nb = n_elements(pos)

;  im = fltarr(ns,nl,nb)
;  for i= 0,nb-1 do begin
;  im [*,*,i]=ENVI_GET_DATA(dims=dims, fid=fid, pos=pos[i])
;  endfor

  roi_ids = envi_get_roi_ids(fid=fid) ;On recupere les identifiant des rois
  nbroi_=size(roi_ids,/dimensions) ;Mise en memoire du nombre de rois
  nbroi=nbroi_[0]

 Openw, unitsortieroi, fileout, /GET_LUN

  For k=0,nbroi-1 Do begin

    addr=envi_get_roi(roi_ids[k])
    sz_addr = SIZE(addr,/dimension)
    n_pt=sz_addr[0]

    y = addr / ns
    x = addr - y * ns

  im = envi_get_roi_data(roi_ids[k], addr = addr, fid=fid, pos=pos)

    l=float(0)
    While l le n_pt-1 Do begin; Boucle sur les addresses
        writeu,unitsortieroi,float(k+1); On ecrit le numéro de la classe
        for t=0, nb-1 do begin; On écrit le CN du pixel
            if nb eq 1 then begin
            writeu,unitsortieroi, im[l]
            endif else begin
             writeu,unitsortieroi, im[t,l]
            endelse
      endfor
      l=l+1
      endwhile
  endfor

free_lun, unitsortieroi

End

pro addr_to_bin,fileout,fid, wh_mask,roi_opt,pos; Fonction qui convertie un mask au format libsvm
;si roi_opt = 1 alors on gere un roi sinon mask classique
COMMON SHARE
  envi_file_query, fid, ns=ns, nl=nl, dims=dims ;On recupere les informations de taille de l_image

  Openw, unitsortie, fileout, /GET_LUN ;On ouvre le fichier de sortie
  writeu,unitsortie, pos
    ;writeu,unitsortie, float(pos)
  if (roi_opt eq 0) then begin; cas d'utilisation d'un masque
  ;    sz_wh = SIZE(wh_mask)
  ;     nl_wh = sz_wh[1]
       writeu,unitsortie, wh_mask
         free_lun, unitsortie

  a = lonarr(n_elements(wh_mask))
  Openr, unittest, fileout, /GET_LUN ;On ouvre le fichier de sortie
    readu,unittest, a
 ;   print, a[0:20]
    free_lun, unittest
;    print, "ok"

   endif else begin
      roi_ids = envi_get_roi_ids(fid=fid) ;On recupere les identifiant des rois
      nbroi_=size(roi_ids,/dimensions) ;Mise en memoire du nombre de rois
      nbroi=nbroi_[0]

      For k=0,nbroi-1 Do begin; boucle pour connaitre le nombre de point de l'ensemble des ROIs
          addr=envi_get_roi(roi_ids[k])
          if(k eq 0) then begin
              all_addr = addr
          endif else begin
              all_addr = [all_addr,addr]
          endelse
       endfor
       n_pt_all= n_elements(all_addr)
       all_addr = all_addr[sort(all_addr)]
       writeu,unitsortie, all_addr
   endelse
free_lun, unitsortie


End

function script_svm,rep_racine,file_script,file_classif,file_input,addr_file
COMMON SHARE
COMMON SHARE2
svm_param=''; Variable qui stocke les parametres svm
range_file = rep_racine+'range'
input_bin = rep_racine + 'training.bin'
input_bin_norm = rep_racine + 'training_norm.bin'
svm_model_file = rep_racine + 'svm_model.txt'

Openw, unitsvm,  rep_racine+file_script, /GET_LUN
;printf, unitsvm, 'cd '+rep_racine

;Normalisation du fichier d_entrainement
;printf, unitsvm, 'svm-scale-bin  '+range_file+  ' '+input_bin+' '+input_bin_norm+' '+strn(Npolar)

;;;;;;TEMP
cmd=''
cmd = 'svm-scale-bin  0.1 '+range_file+  ' '+input_bin+' '+input_bin_norm+' '+strn(nb_classif)
    spawn,cmd


;Entrainement du ROI
;Pour les reglages CF fichier LIBSVM
; kernel_type = ''
; READ, kernel_type, PROMPT='Quel noyaux utilisez vous : LINEAIRE , POLYNOMIAL ou RBF ?'
; ;if ((kernel_type ne 'LINEAIRE') or (kernel_type ne 'POLYNOMIAL') or (kernel_type ne 'RBF'))  then exit
; ;if (kernel_type ne 'LINEAIRE') or  (kernel_type ne 'POLYNOMIAL') or (kernel_type ne 'RBF') then exit
; if kernel_type eq 'LINEAIRE' then begin
;   cost=''
;   READ, cost, PROMPT='Quel cout voulez vous utilisez ?'
;   printf,unitsvm,'svm-train-bin -t 0 -c '+ cost +' '+input_bin_norm+ '  '+svm_model_file+' '+strn(Npolar)
;   svm_param = svm_param + 'noy_lin_cout_' + cost
; endif
;
; if kernel_type eq 'POLYNOMIAL' then begin
;   degre = ''
;   READ, degre, PROMPT='Quel degre voulez vous utilisez ?'
;   cost=''
;   READ, cost, PROMPT='Quel cout voulez vous utilisez ?'
;   printf,unitsvm,'svm-train -t 1 -d ' + degre +' -c '+ cost  +' '+input_bin_norm+ '  '+svm_model_file+' '+strn(Npolar)
;   svm_param = svm_param + 'noy_poly_degre_' + degre + '_cout_' + cost
; endif

; if kernel_type eq 'RBF' then begin

    if CV eq 1 then begin
      min_c = alog(best_c)/alog(2) - 4  & if min_c lt 10  then min_c = 10
      max_c = alog(best_c)/alog(2) + 4 & if max_c gt 16  then max_c = 16
      if max_c lt min_c  then max_c = min_c
      step_c = 2

      min_g = alog(best_g)/alog(2) - 4
      max_g = alog(best_g)/alog(2) + 4 & if max_g gt 1 then max_g = 1
      if max_g lt min_g  then min_g = max_g
      step_g = 2
      cmd =''
      cmd = 'grid_polsarpro  '+'-log2c '+strn(min_c)+' '+strn(max_c)+' '+strn(step_c)+$
		' -log2g '+strn(min_g)+' '+strn(max_g)+' '+strn(step_g)+' -out '+rep_racine+'cv.txt '+$
		'-png '+rep_racine+'cv.png '+'-svmtrain '+svm_train_path+' -gnuplot '+gnuplot_path+' '+$
		input_bin_norm+ '  '+svm_model_file+' '+strn(nb_classif)
      spawn, cmd

;;;;;;On lit le fichier txt de cv pour en extraire les meilleurs paramètres
      cv_tab = fltarr(2,50)
      perf_tab = fltarr(50)
      c = 0.
      g = 0.
      perf = 0.
      count = 0
      OPENR, lun, rep_racine+'cv.txt', /GET_LUN
      WHILE (NOT EOF(lun)) DO BEGIN
        READF, lun, c, g, perf
        cv_tab[0,count] = 2^c
        cv_tab[1,count] = 2^g
        perf_tab(count) = perf
        count = count + 1
      ENDWHILE
      free_lun,lun
      cv_tab = cv_tab[*,0:count-1]
      perf_tab = perf_tab[0:count-1]

      perf_sort = sort(perf_tab)
      best_c = cv_tab[0,perf_sort(count-1)]
      best_g = cv_tab[1,perf_sort(count-1)]
    endif
  gamma = string(best_g)
  cost= string(best_c)

  printf,unitsvm,'svm-train-bin -b 1 -t 2 -g ' + gamma +' -c '+ cost  +' '+input_bin_norm+ '  '+svm_model_file+' '+strn(nb_classif)
  svm_param = svm_param + 'noy_rbf_gamma_' + gamma + '_cout_' + cost


;Prediction du fichier image
printf, unitsvm, 'svm-predict-bin_prob 1 '+svm_model_file+' '+range_file+' '+file_classif+' '+file_input+' '+addr_file+' '+strn(nb_classif)+' '+strn(ns)+' '+strn(nl)

;writeu, unit
free_lun, unitsvm

if !VERSION.OS_FAMILY eq 'unix' then begin
	spawn, 'sh '+rep_racine+file_script
endif else begin
	spawn, rep_racine+file_script,/noshell
endelse
return , svm_param
END

PRO get_size, im, sx, sy

COMPILE_OPT IDL2

sz = SIZE(im)
sx = sz[1]
sy = (1 EQ sz[0]) ? 1 : sz[2]

END

function strn, number, LENGTH = length, PADTYPE = padtype, PADCHAR = padchar, $
                       FORMAT = Format
;+
; NAME:
; STRN
; PURPOSE:
; Convert a number to a string and remove padded blanks.
; EXPLANATION:
; The main and original purpose of this procedure is to convert a number
; to an unpadded string (i.e. with no blanks around it.)  However, it
; has been expanded to be a multi-purpose formatting tool.  You may
; specify a length for the output string; the returned string is either
; set to that length or padded to be that length.  You may specify
; characters to be used in padding and which side to be padded.  Finally,
; you may also specify a format for the number.  NOTE that the input
; "number" need not be a number; it may be a string, or anything.  It is
; converted to string.
;
; CALLING SEQEUNCE:
; tmp = STRN( number, [ LENGTH=, PADTYPE=, PADCHAR=, FORMAT = ] )
;
; INPUT:
; NUMBER    This is the input variable to be operated on.  Traditionally,
;    it was a number, but it may be any scalar type.
;
; OPTIONAL INPUT:
; LENGTH    This KEYWORD specifies the length of the returned string.
;   If the output would have been longer, it is truncated.  If
;   the output would have been shorter, it is padded to the right
;   length.
; PADTYPE   This KEYWORD specifies the type of padding to be used, if any.
;   0=Padded at End, 1=Padded at front, 2=Centered (pad front/end)
;   IF not specified, PADTYPE=1
; PADCHAR   This KEYWORD specifies the character to be used when padding.
;   The default is a space (' ').
; FORMAT    This keyword allows the FORTRAN type formatting of the input
;   number (e.g. '(f6.2)')
;
; OUTPUT:
; tmp       The formatted string
;
; USEFUL EXAMPLES:
; print,'Used ',strn(stars),' stars.'  ==> 'Used 22 stars.'
; print,'Attempted ',strn(ret,leng=6,padt=1,padch='0'),' retries.'
;   ==> 'Attempted 000043 retries.'
; print,strn('M81 Star List',length=80,padtype=2)
;   ==> an 80 character line with 'M81 Star List' centered.
; print,'Error: ',strn(err,format='(f15.2)')
;   ==> 'Error: 3.24'     or ==> 'Error: 323535.22'
;
; HISTORY:
; 03-JUL-90 Version 1 written by Eric W. Deutsch
; 10-JUL-90 Trimming and padding options added         (E. Deutsch)
; 29-JUL-91 Changed to keywords and header spiffed up     (E. Deutsch)
; Ma7 92 Work correctly for byte values (W. Landsman)
; 19-NOV-92 Added Patch to work around IDL 2.4.0 bug which caused an
; error when STRN('(123)') was encountered.            (E. Deutsch)
; Converted to IDL V5.0   W. Landsman   September 1997
;-
 On_error,2
  if ( N_params() LT 1 ) then begin
    print,'Call: IDL> tmp=STRN(number,[length=,padtype=,padchar=,format=])'
    print,"e.g.: IDL> print,'Executed ',strn(ret,leng=6,padt=1,padch='0'),' retries.'"
    return,''
    endif
  if (N_elements(padtype) eq 0) then padtype=1
  if (N_elements(padchar) eq 0) then padchar=' '
  if (N_elements(Format) eq 0) then Format=''

  padc = byte(padchar)
  pad = string(replicate(padc[0],200))

  ss=size(number) & PRN=1 & if (ss[1] eq 7) then PRN=0
  if ( Format EQ '') then tmp = strtrim( string(number, PRINT=PRN),2) $
    else tmp = strtrim( string( number, FORMAT=Format, PRINT=PRN),2)

  if (N_elements(length) eq 0) then length=strlen(tmp)

  if (strlen(tmp) gt length) then tmp=strmid(tmp,0,length)

  if (strlen(tmp) lt length) and (padtype eq 0) then begin
    tmp = tmp+strmid(pad,0,length-strlen(tmp))
    endif

  if (strlen(tmp) lt length) and (padtype eq 1) then begin
    tmp = strmid(pad,0,length-strlen(tmp))+tmp
    endif

  if (strlen(tmp) lt length) and (padtype eq 2) then begin
    padln=length-strlen(tmp) & padfr=padln/2 & padend=padln-padfr
    tmp=strmid(pad,0,padfr)+tmp+strmid(pad,0,padend)
    endif

  return,tmp
end

function stats_classif_gen,file_classif,file_stat,file_roi

envi_open_file, file_classif,r_fid=fid ; On ouvre le fichier de classification

envi_delete_rois, /all ; On efface d'envi tout les ROI deja ouvert
ENVI_RESTORE_ROIS, file_roi ; On restore le ROI de controle


roi_ids = envi_get_roi_ids(fid=fid,roi_names=roi_names)
envi_file_query, fid, dims=dims,ns=ns, nl=nl, nb=nb, $
    num_classes=num_classes
pos  = [0]
class_ptr = lindgen(n_elements(roi_ids)) + 1


  ;
  ; Call the doit
  ;
;print, 'pause'
  envi_doit, 'class_confusion_doit', $
    cfid=fid, cpos=pos, dims=dims, $
    roi_ids=roi_ids, class_ptr=class_ptr, $
    /rpt_commission, to_screen=0, $
    calc_percent=1, commission=commission, $
    omission=omission, matrix=matrix, $
    kappa_coeff=kappa_coeff, accuracy=accuracy

sz=size(matrix)
ns_conf=sz[1]
nl_conf=sz[2]

matrix_=matrix[*,1:nl_conf-1]

nb_class=n_elements(roi_names)

;stockage du nom des classes
class_names=strarr(nb_class)
for i=0,nb_class-1 do begin
result=strsplit(roi_names[i],/EXTRACT)
class_names[i]=result[0]
endfor
;max_char=max(strlen(class_names))
;if max_char LT 5 then max_char=5

matrix_percent=fltarr(nb_class+1,nb_class+1)
;;;;;;;;;;;Conversion en pourcent de la matrice de confusion
for k=0,nb_class-1 do begin;passage en pourcent de la matrice principale
  matrix_percent[k,0:nb_class-1]=matrix_[k,0:nb_class-1]/matrix_[k,nb_class]
Endfor

for l=0,nb_class-1 do begin;pourcent de la derniere colonne
  matrix_percent[nb_class,l]=matrix_[l,nb_class]/matrix_[nb_class,nb_class]
Endfor
  matrix_percent[*,nb_class]=TOTAL(matrix_percent[*,0:nb_class-1],2)

;nb_truth=matrix_percent[nb_class,nb_class]
nb_truth=1.*nb_class
;print, nb_truth
s1=0.;premier element somme de Kappa
s2=0.;deuxieme element somme de kappa
for i=0,nb_class-1 do begin
  s1=s1+matrix_percent[i,i]
Endfor
mpa=s1/nb_class;moyenne de la diagonale

for j=0,nb_class-1 do begin
  s2=s2+matrix_percent[j,nb_class]*matrix_percent[nb_class,j]
 ; print, matrix_percent[j,nb_class]
Endfor
kappa_percent=(nb_truth*s1-s2)/(nb_truth^(2)-s2)

;;;;ecriture en texte des matrice de confusion
confusion_pixel_text=strarr(nb_class+2,nb_class+2)
confusion_percent_text=strarr(nb_class+2,nb_class+2)

For i=1,nb_class do begin
  confusion_pixel_text[0,i]=class_names[i-1]
  confusion_percent_text[0,i]=class_names[i-1]
endfor
confusion_pixel_text[0,nb_class+1]='Total'
confusion_percent_text[0,nb_class+1]='Total'

For i=1,nb_class do begin
  confusion_pixel_text[i,0]=class_names[i-1]
  confusion_percent_text[i,0]=class_names[i-1]
endfor
confusion_pixel_text[nb_class+1,0]='Total'
confusion_pixel_text[1:nb_class+1,1:nb_class+1]=string(fix(matrix_[*,*]))
confusion_percent_text[1:nb_class+1,1:nb_class+1]=string(fix(matrix_[*,*]))

confusion_percent_text[nb_class+1,0]='Total'
confusion_percent_text[1:nb_class+1,1:nb_class+1]=string(matrix_percent[*,*])

openw,unitstats,file_stat+'_training_stats.txt',/get_lun


printf,unitstats,'File classif : ', file_classif
printf,unitstats,'File roi : ', file_roi
;printf,unitstats,log_band

printf,unitstats,''
;Ecriture de la matrice de confusion en pixel
printf,unitstats,'Confusion matrix in pixel'
for j=0,nb_class+1 do begin
  for i=0,nb_class+1 do begin
    if i eq nb_class+1 then begin
      if j eq 0 then begin
        printf,unitstats,format='(A14)',strn(confusion_pixel_text[i,j])
      endif else begin
        printf,unitstats,format='(A14)',strn(confusion_pixel_text[i,j],length=6)
      endelse
    endif else begin
      if j eq 0 then begin
        printf,unitstats,format='($,A14,A1)',strn(confusion_pixel_text[i,j]),string(9B)
      endif else begin
        if i eq 0 then begin
          printf,unitstats,format='($,A14,A1)',strn(confusion_pixel_text[i,j],length=14),string(9B)
        endif else begin
          printf,unitstats,format='($,A14,A1)',strn(confusion_pixel_text[i,j],length=6),string(9B)
        endelse
      endelse
    endelse
  endfor
endfor
printf,unitstats,''
;Ecriture de la matrice de confusion en pourcent
printf,unitstats,'Confusion matrix in percent'
for j=0,nb_class+1 do begin
  for i=0,nb_class+1 do begin
    if i eq nb_class+1 then begin
      if j eq 0 then begin
        printf,unitstats,format='(A14)',strn(confusion_percent_text[i,j])
      endif else begin
        printf,unitstats,format='(A14)',strn(confusion_percent_text[i,j],length=7)
      endelse
    endif else begin
      if j eq 0 then begin
        printf,unitstats,format='($,A14,A1)',strn(confusion_percent_text[i,j]),string(9B)
      endif else begin
        if i eq 0 then begin
          printf,unitstats,format='($,A14,A1)',strn(confusion_percent_text[i,j],length=14),string(9B)
        endif else begin
          printf,unitstats,format='($,A14,A1)',strn(confusion_percent_text[i,j],length=7),string(9B)
        endelse
      endelse
    endelse
  endfor
endfor
printf,unitstats,''
;Ecriture de Producer accuracy PA et User Accuracy UA
printf,unitstats,format='(A14,A1,A14,A1,A14)','Class',string(9B),'PA',string(9B),'UA'
for i=1,nb_class-2 do begin
  printf,unitstats,format='(A14,A1,A14,A1,A14)',strn(confusion_percent_text[0,i]),string(9B),strn(confusion_percent_text[i,i],length=7),string(9B),$
    strn(matrix_[i-1,i-1]/matrix_[nb_class,i-1],length=7)
endfor
  printf,unitstats,format='(A14,A1,A14,A1,A14)',strn(confusion_percent_text[0,nb_class-1]),string(9B),strn(confusion_percent_text[nb_class-1,nb_class-1],length=7),string(9B),$
    strn(matrix_[nb_class-1,nb_class-1]/matrix_[nb_class,nb_class-1],length=7)
  printf,unitstats,format='(A14,A1,A14,A1,A14)',strn(confusion_percent_text[0,nb_class]),string(9B),strn(confusion_percent_text[nb_class,nb_class],length=7),string(9B),$
    strn(matrix_[nb_class-2,nb_class-2]/matrix_[nb_class,nb_class-2],length=7)


printf,unitstats,''
;Ecriture des indices globaux
printf,unitstats, format='(A17,A1,A7)','kappa : ',string(9B),strn(kappa_coeff,length=7)
printf, unitstats, format='(A17,A1,A7)', 'kappa percent : ',string(9B),strn(kappa_percent,length=7)
printf, unitstats, format='(A17,A1,A7)','mpa : ', string(9B),strn(mpa,length=7)
free_lun,unitstats
envi_file_mng, id=fid, /remove
return,mpa

END