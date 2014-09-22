#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <math.h>
#include "svm.h"
/* Effacer les fichier temporaire comme training et addr
 * 
 * 
 * 
 * 
 */




//POLSARPRO
struct svm_node *x;
int max_nr_attr = 64;
long memory_pixel = 2 * 100 * 100;// Number of pixel for one block in memory

struct svm_model* model;
int predict_probability=0;

static char *line = NULL;

double *feature_max;
double *feature_min;

double lower=-1.0,upper=1.0;

double scale(int index, double value);
void restore_scale_param(FILE *range_restore, long Npolar);



/* ******* POLSARPRO FUNCTION ****** */
void edit_error(char *s1,char *s2);
/*******************************************************************************
Routine  : edit_error
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Displays an error message and exits the program
*-------------------------------------------------------------------------------
Inputs arguments :
s1    : message to be displayed
s2    : message to be displayed
Returned values  :
void
*******************************************************************************/
void edit_error(char *s1, char *s2)
{
    printf("\n A processing error occured ! \n %s%s\n", s1, s2);
    exit(1);
}

void exit_input_error(int line_num)
{
	fprintf(stderr,"Wrong input format at line %d\n", line_num);
	exit(1);
}
/*******************************************************************************
Routine  : vector_float
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Creates and allocates memory for a vector of float elements
*-------------------------------------------------------------------------------
Inputs arguments :
nrh   : number of float
Returned values  :
m     : vector pointer (float *)
*******************************************************************************/
float *vector_float(int nrh)
{
    int ii;
    float *m;

    m = (float *) malloc((unsigned) (nrh + 1) * sizeof(float));
    if (!m)
	edit_error("allocation failure 1 in vector_float()", "");

    for (ii = 0; ii < nrh; ii++)
	m[ii] = 0;
    return m;
}

/*******************************************************************************
Routine  : free_vector_float
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Erases a vector and disallocates memory for a vector
of float elements
*-------------------------------------------------------------------------------
Inputs arguments :

Returned values  :
void
*******************************************************************************/
void free_vector_float(float *m)
{
    free((float *) m);
}

/*******************************************************************************
Routine  : matrix_float
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Creates and allocates memory for a 2D matrix of float elements
*-------------------------------------------------------------------------------
Inputs arguments :
nrh   : number of lines
nch   : number of rows
Returned values  :pr
m     : matrix pointer (float **)
*******************************************************************************/
float **matrix_float(int nrh, int nch)
{
    int i, j;
    float **m;

    m = (float **) malloc((unsigned) (nrh) * sizeof(float *));
    if (!m)
	edit_error("allocation failure 1 in matrix()", "");

    for (i = 0; i < nrh; i++) {
	m[i] = (float *) malloc((unsigned) (nch) * sizeof(float));
	if (!m[i])
	    edit_error("allocation failure 2 in matrix()", "");
    }
    for (i = 0; i < nrh; i++)
	for (j = 0; j < nch; j++)
	    m[i][j] = (float) 0.;
    return m;
}

/*******************************************************************************
Routine  : free_matrix_float
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Erases a matrix and disallocates memory for a 2D matrix of float elements
*-------------------------------------------------------------------------------
Inputs arguments :
nrh   : number of lines
Returned values  :
void
*******************************************************************************/
void free_matrix_float(float **m, int nrh)
{
    int i;
    for (i = nrh - 1; i >= 0; i--)
	free((float *) (m[i]));
}
/* ******* POLSARPRO FUNCTION ****** */

void predict(FILE *input, FILE *output, FILE *output_w2, FILE *output_prob,int predict_probability, FILE *addr, int Ncol, int Nlig, long Npolar)
{
	int svm_type=svm_get_svm_type(model);
	int nr_class=svm_get_nr_class(model);
	double *prob_estimates=NULL;
	int i,j,k,l,num_block,p,n,count;
	int Nband[Npolar];
	long n_addr = 0,m=0, n_total_band, offset=0;
	long max_num_pixel, num_rest_pixel, n_img_pixel = (long)Ncol * (long)Nlig;
	float buff_float, zero = 0;
	float **V_pol_rest, **V_pol_block, *v_pol_buff;
	long int *tab_addr, buff_long_int;
	float *output_label;
	double *w2_predict;
	float **w2_predict_out, *mean_dist, *max_prob, **prob_estimates_out;
	
	
	max_num_pixel = (long)floor(memory_pixel /((long)4 * Npolar));
	
	for(i=0; i< n_img_pixel; i++){// We initiaite the output classification file with '0' value
		fwrite(&zero, sizeof(float), 1, output);
	}
	rewind(output);
	
/*	for(i=0; i< n_img_pixel*(nr_class*(nr_class-1)/2 +1) ; i++){// We initiaite the output classification file with '0' value
		fwrite(&zero, sizeof(float), 1, output_w2);
	}
	rewind(output_w2);
*/
	if(predict_probability)
	{
		printf("Predict prob!!!!\n");
		for(i=0; i< n_img_pixel*(nr_class + 1) ; i++){// We initiaite the output classification file with '0' value
			fwrite(&zero, sizeof(float), 1, output_prob);
		}
		rewind(output_prob);
		
		if (svm_type==NU_SVR || svm_type==EPSILON_SVR)
			printf("Prob. model for test data: target value = predicted value + z,\nz: Laplace distribution e^(-|z|/sigma)/(2sigma),sigma=%g\n",svm_get_svr_probability(model));
		else
		{
			int *labels=(int *) malloc(nr_class*sizeof(int));
			svm_get_labels(model,labels);
			prob_estimates = (double *) malloc(nr_class*sizeof(double));
			//fprintf(output,"labels");		
			//for(j=0;j<nr_class;j++)
			//	printf(" %d\n",labels[j]);
				//fprintf(output," %d",labels[j]);
			//fprintf(output,"\n");
			free(labels);
		}
	}

	while(fread(&buff_long_int, sizeof(long int), 1, addr)!=0){ // We read the addr file to know the number of pixel to be classified
		n_addr++;
	}
	n_addr = n_addr - Npolar;
	rewind(addr);
	tab_addr = (long int *) malloc((long int) (n_addr) * sizeof(long int));

	for(i=0; i<Npolar;i++){
		fread(&buff_long_int, sizeof(long int), 1, addr);
		Nband[i] = (int)buff_long_int;
	}
	i=0;


	while(fread(&tab_addr[i], sizeof(long int), 1, addr)!=0){ // We read the addr of each classified pixel
//hde
//printf("tab_addr[%d]:%d\n",i,tab_addr[i]);

		i++;

	}
//hde
int min,max;
min=tab_addr[0];
max=min;
for (i=0;i<n_addr;i++)
{
	if (tab_addr[i]>max) {max=tab_addr[i];}
	if (tab_addr[i]<min) {min=tab_addr[i];}
}
printf("min:%d; max:%d\n",min,max);
// fin HDE

	// We compute the necessary number of block and remaining pixel
	num_block = (int)floor(n_addr /max_num_pixel);
	num_rest_pixel = n_addr - num_block * max_num_pixel;
	printf("num_block: %i\n",num_block);

	/////////////////////////////////////////////////Ajouter boucle de lecture des float input pour ensuite calculer le
	//nb de bande total initial pour faire une lecutre par bloc de bande puis extraire celle qui sont interessante
	while(fread(&buff_float, sizeof(float), 1, input)!=0){ 
		m++;
	}
	rewind(input);
	
	if(num_block > 0){//Loop on the block
		V_pol_block = matrix_float((int)max_num_pixel,(int)Npolar);
		output_label = vector_float((int)max_num_pixel);
	//	mean_dist = vector_float((int)max_num_pixel);
	//	w2_predict_out = matrix_float((int)max_num_pixel,nr_class*(nr_class-1)/2);
		prob_estimates_out = matrix_float((int)max_num_pixel,nr_class);
		max_prob = vector_float((int)max_num_pixel);
		for (i=0; i<num_block; i++){	// blocs pour l'optimisation accès disque
			for (j=0; j< max_num_pixel; j++){
				for (k=0; k<Npolar; k++){	
					// pointe sur le pixel col,lig, k(bande), selon la bande
					offset = (long)(sizeof(float)) * (Nband[k] * n_img_pixel + tab_addr[i*max_num_pixel + j]);
					fseek(input, offset, SEEK_SET); //place le pointeur à l'offset calculé avant qui s'appelle offset ! 
					fread(&V_pol_block[j][k], sizeof(float), 1, input);

				}
			}
			for (j=0; j< max_num_pixel; j++){
				for (k=0; k<Npolar; k++){
					if(k>=max_nr_attr-1)	// need one more for index = -1
					{
						max_nr_attr *= 2;
						x = (struct svm_node *) realloc(x,max_nr_attr*sizeof(struct svm_node));
					}
					x[k].index = k+1;
					x[k].value = scale(k, (double)V_pol_block[j][k]);
				}
				x[k].index = -1;
				double predict_label;
				
				if (predict_probability && (svm_type==C_SVC || svm_type==NU_SVC))
				{
					//printf("Predict prob if block!!!!\n");
					predict_label = svm_predict_probability(model,x,prob_estimates);
					
					w2_predict = svm_w2(model,x);				
					
					output_label[j] = (float)predict_label;
					
	//				mean_dist[j] = 0.;
					count = 0;
					l=0;
					max_prob[j] = 0.;
					for(p=0;p<nr_class;p++){
						for(n=p+1;n<nr_class;n++){
		//					w2_predict_out[j][l] =(float)w2_predict[l];
						//	printf("w2_predict[%i] : %g\n",w2_predict[l]);
							if(p+1 == output_label[j] || n+1 == output_label[j]){
			//					mean_dist[j] = mean_dist[j] + w2_predict_out[j][l];
								count = count + 1;
							}
							l++;
						}
						prob_estimates_out[j][p] = (float)prob_estimates[p];
						if(max_prob[j] < prob_estimates_out[j][p] ){
							max_prob[j] = prob_estimates_out[j][p];
						}
					}
		//			mean_dist[j] = mean_dist[j] / (float)count;
				}
				else
				{
					predict_label = svm_predict(model,x);
					
					w2_predict = svm_w2(model,x);
					
					
					
					output_label[j] = (float)predict_label;
					
		//			mean_dist[j] = 0.;
					count = 0;
					l=0;
					for(p=0;p<nr_class;p++){
						for(n=p+1;n<nr_class;n++){
			//				w2_predict_out[j][l] =(float)w2_predict[l];
							
							if(p+1 == output_label[j] || n+1 == output_label[j]){
				//			mean_dist[j] = mean_dist[j] + w2_predict_out[j][l];
								count = count + 1;
							}
							l++;
						}
					}
		//			mean_dist[j] = mean_dist[j] / (float)count;
						
				
						
				}
			}/* pixels block */

			for (j=0; j< max_num_pixel; j++){ // On ecrit le fichier de classif
				offset = (long)(sizeof(float)) * tab_addr[i*max_num_pixel + j];
					fseek (output, offset, SEEK_SET);
					fwrite(&output_label[j], sizeof(float), 1, output);
					
					
			}
/*			for (l=0; l< nr_class*(nr_class-1)/2; l++){ // On ecrit les cartes de distances
				for (j=0; j< max_num_pixel; j++){
					offset = (long)(sizeof(float)) * tab_addr[i*max_num_pixel + j];
					fseek(output_w2, offset + n_img_pixel * sizeof(float) * l, SEEK_SET);
					fwrite(&w2_predict_out[j][l],  sizeof(float), 1, output_w2);		
				}			
			}
			
			for (j=0; j< max_num_pixel; j++){ // On ecrit la distance moyenne
				offset = (long)(sizeof(float)) * tab_addr[i*max_num_pixel + j];
				fseek(output_w2, offset + n_img_pixel * sizeof(float) * (nr_class*(nr_class-1)/2), SEEK_SET);// on ecrit la distance moyenne parmi les classif bianaire renvoyant le label final
				fwrite(&mean_dist[j],  sizeof(float), 1, output_w2);
			}
*/			
			if(predict_probability){
				//printf("Predict prob fin if block ecriture!!!!\n");
				for (l=0; l< nr_class; l++){ // On ecrit les cartes de probabilité
					for (j=0; j< max_num_pixel; j++){
						offset = (long)(sizeof(float)) * tab_addr[i*max_num_pixel + j];
						fseek(output_prob, offset + n_img_pixel * sizeof(float) * l, SEEK_SET);
						fwrite(&prob_estimates_out[j][l],  sizeof(float), 1, output_prob);		
					}			
				}
				
				for (j=0; j< max_num_pixel; j++){
						offset = (long)(sizeof(float)) * tab_addr[i*max_num_pixel + j];
						fseek(output_prob, offset + n_img_pixel * sizeof(float) * nr_class, SEEK_SET);
						fwrite(&max_prob[j],  sizeof(float), 1, output_prob);		
					}	
			}

		}/* Loop over the blocks*/
		free_matrix_float(V_pol_block, max_num_pixel);
	//	free_matrix_float(w2_predict_out, max_num_pixel);
		free_matrix_float(prob_estimates_out, max_num_pixel);
		free_vector_float(output_label);
	//	free_vector_float(mean_dist);
		free(w2_predict);
		free_vector_float(max_prob);
		printf("FREE block: %i\n",num_block);
	}else{
		printf("PAS DE BLOCK\n");
	}
	if(num_rest_pixel > 0){// Loop on the remaining pixel
		V_pol_rest = matrix_float((int)num_rest_pixel,(int)Npolar);/* Vector of polarimetrics indicators  for the remaining pixel */
		output_label = vector_float((int)num_rest_pixel);
	//	w2_predict_out = matrix_float((int)num_rest_pixel,nr_class*(nr_class-1)/2);
	//	mean_dist = vector_float((int)num_rest_pixel);
		prob_estimates_out = matrix_float((int)num_rest_pixel,nr_class);
		max_prob = vector_float((int)max_num_pixel);
		for (j=0; j< num_rest_pixel;j++){
			for (k=0; k<Npolar; k++){	
				offset = (long)(sizeof(float)) * (Nband[k] * n_img_pixel + tab_addr[num_block*max_num_pixel + j]);
				fseek (input, offset , SEEK_SET);
				fread(&V_pol_rest[j][k], sizeof(float), 1, input);
				
//hde
//printf("valeur pixel a adresse %d et pour bande %d: %d\n", tab_addr[num_block*max_num_pixel + j],k,V_pol_rest[j][k]);
			}
		}
		for (j=0; j< num_rest_pixel;j++){
			for (k=0; k<Npolar; k++){
				if(k>=max_nr_attr-1)	// need one more for index = -1
				{
					max_nr_attr *= 2;
					x = (struct svm_node *) realloc(x,max_nr_attr*sizeof(struct svm_node));
				}
				x[k].index = k+1;
				x[k].value = scale(k, (double)V_pol_rest[j][k]);
			}
			x[k].index = -1;
			double predict_label;
			if (predict_probability && (svm_type==C_SVC || svm_type==NU_SVC))
			{
				//printf("Predict prob if fin apres block!!!!\n");
				predict_label = svm_predict_probability(model,x,prob_estimates);
				 w2_predict = svm_w2(model,x);				
					
				output_label[j] = (float)predict_label;
					
		//		mean_dist[j] = 0.;
				count = 0;
				l=0;
				max_prob[j] = 0.;
				for(p=0;p<nr_class;p++){
					for(n=p+1;n<nr_class;n++){
				//		w2_predict_out[j][l] =(float)w2_predict[l];
					//	printf("w2_predict[%i] : %g\n",l,w2_predict[l]);
					//	printf("w2_predict_out[%i][%i] : %g\n",j,l,w2_predict_out[j][l]);
						if(p+1 == output_label[j] || n+1 == output_label[j]){
			//				mean_dist[j] = mean_dist[j] + w2_predict_out[j][l];
							count = count + 1;
						}
						l++;
					}
					prob_estimates_out[j][p] = (float)prob_estimates[p];
					if(max_prob[j] < prob_estimates_out[j][p] ){
							max_prob[j] = prob_estimates_out[j][p];
						}
				}
		//		mean_dist[j] = mean_dist[j] / (float)count;
				//printf("mean_dist[%i],%f\n",j,mean_dist[j]);
			}
			else
			{
				predict_label = svm_predict(model,x);
				
				w2_predict = svm_w2(model,x);
					
				
				
				output_label[j] = (float)predict_label;
					
		//		mean_dist[j] = 0.;
				count = 0;
				l=0;
				for(p=0;p<nr_class;p++){
					for(n=p+1;n<nr_class;n++){
			//			w2_predict_out[j][l] =(float)w2_predict[l];
						
						if(p+1 == output_label[j] || n+1 == output_label[j]){
		//					mean_dist[j] = mean_dist[j] + w2_predict_out[j][l];
							count = count + 1;
						}
						l++;
					}
				}
		//		mean_dist[j] = mean_dist[j] / (float)count;
			}
		}
		for (j=0; j< num_rest_pixel; j++){
				offset = (long)(sizeof(float)) * (tab_addr[num_block*max_num_pixel + j]);
					fseek (output, offset, SEEK_SET);
					fwrite(&output_label[j], sizeof(float), 1, output);
					
					
			}
/*			for (l=0; l< nr_class*(nr_class-1)/2; l++){
				for (j=0; j< num_rest_pixel; j++){
					offset = (long)(sizeof(float)) * (tab_addr[num_block*max_num_pixel + j]);
					fseek(output_w2, offset + n_img_pixel * sizeof(float) * l, SEEK_SET);
					fwrite(&w2_predict_out[j][l],  sizeof(float), 1, output_w2);		
				}			
			}
			
			for (j=0; j< num_rest_pixel; j++){
				offset = (long)(sizeof(float)) * (tab_addr[num_block*max_num_pixel + j]);
				fseek(output_w2, offset + n_img_pixel * sizeof(float) * (nr_class*(nr_class-1)/2), SEEK_SET);// on ecrit la distance moyenne parmi les classif bianaire renvoyant le label final
				fwrite(&mean_dist[j],  sizeof(float), 1, output_w2);
			}
*/			
			
			if(predict_probability){
				//printf("Predict prob if fin apres blockeCRITUR!!!!!!!\n");
				for (l=0; l< nr_class; l++){ // On ecrit les cartes de probabilité
					for (j=0; j< num_rest_pixel; j++){
						offset = (long)(sizeof(float)) * (tab_addr[num_block*max_num_pixel + j]);
						fseek(output_prob, offset + n_img_pixel * sizeof(float) * l, SEEK_SET);
						fwrite(&prob_estimates_out[j][l],  sizeof(float), 1, output_prob);	
						//printf("prob_estimates_out[%i][%i] : %f\n", j, l, prob_estimates_out[j][l]);	
					}			
				}
				for (j=0; j< num_rest_pixel; j++){
						offset = (long)(sizeof(float)) * (tab_addr[num_block*max_num_pixel + j]);
						fseek(output_prob, offset + n_img_pixel * sizeof(float) * nr_class, SEEK_SET);
						fwrite(&max_prob[j],  sizeof(float), 1, output_prob);	
					}	
				
			}

		free_matrix_float(V_pol_rest, num_rest_pixel);
	//	free_matrix_float(w2_predict_out, num_rest_pixel);
		free_matrix_float(prob_estimates_out, num_rest_pixel);
		free_vector_float(output_label);
		free(w2_predict);
	//	free_vector_float(mean_dist);
		free_vector_float(max_prob);
	}/* remaning pixel */
	free(tab_addr);	
	
	if(predict_probability)
		free(prob_estimates);
}

void restore_scale_param(FILE *range_restore, long Npolar)
{
	int idx;
	double fmin, fmax;
	
	feature_max = (double *)malloc((Npolar)* sizeof(double));
	feature_min = (double *)malloc((Npolar)* sizeof(double));

	if (fgetc(range_restore) == 'x') {
	  fscanf(range_restore, "%lf %lf\n", &lower, &upper);


	while(fscanf(range_restore,"%d %lf %lf\n",&idx,&fmin,&fmax)==3)
	{
		if(idx<=Npolar)
		{
			feature_min[idx-1] = fmin;
			feature_max[idx-1] = fmax;
		}
	}
}
	fclose(range_restore);
}

double scale(int index, double value)
{
	/* skip single-valued attribute */
	if(feature_max[index] == feature_min[index])
		return 0;
	if(value == feature_min[index])
		value = lower;
	else if(value == feature_max[index])
		value = upper;
	else
		value = lower + (upper-lower) * 
			(value-feature_min[index])/
			(feature_max[index]-feature_min[index]);
return value;
}

void exit_with_help()
{
	printf(
	"Usage: svm-predict in_dir svm_model_file range_file output_classif number_of_pol_ind input_ind1 input_ind_2 ...\n"
	"options:\n"
	"-b probability_estimates: whether to predict probability estimates, 0 or 1 (default 0); for one-class SVM only 0 is supported\n"
	);
	exit(1);
}

int main(int argc, char **argv)
{
/* Polsarpro Variables */
	char range_file[1024], output_classif[1024],input_envi_file[1024], input_addr_file[1024];
	char output_dist[1024];
	char file_name[1024];
	int Nlig, Ncol, predict_probability;		/* Initial image nb of lines and rows */
	FILE *class_file, *range_restore, *in_file, *in_addr_file,  *output_dist_file, *prob_file;
	long Npolar; /* Number of polarimetrics indicators */

/* Libsvm Variables */
	int i;    

	if (argc >= 10) {
	  predict_probability =  atoi(argv[1]);
	  sprintf(file_name, "%s", argv[2]);
	  if((model=svm_load_model(file_name))==0)
	    {
		fprintf(stderr,"can't open model file %s\n",file_name);
		exit(1);
	    }
	  strcpy(range_file, argv[3]);
	  strcpy(output_classif, argv[4]);
	  strcpy(input_envi_file, argv[5]);
	  strcpy(input_addr_file, argv[6]);
	  Npolar = atoi(argv[7]);
	  Nlig =  atoi(argv[8]);
	  Ncol =  atoi(argv[9]);
	} else {
	fprintf(stderr,"svm-predict  prob svm_model_file range_file output_classif input_envi_file inpu_addr_file number_of_pol_ind num_b1 num_b2 ...\n");
		exit(1);
	}
	printf("\n\n\nfile_name : %s\n",file_name);
	printf("range_file : %s\n",range_file);
	printf("output_classif : %s \n",output_classif);
	printf(" input_envi_file : %s\n",input_envi_file);
	printf(" input_addr_file : %s\n",input_addr_file);
	printf(" Npolar : %ld\n",Npolar);
	printf(" Nlig : %d\n",Nlig);
	printf(" Ncol : %d\n",Ncol);

	//Test INPUT File
	sprintf(file_name, "%s", input_envi_file);
	if ((in_file = fopen(file_name, "rb")) == NULL)
		{
			fprintf(stderr,"Could not open input file : %s\n",file_name);
			exit(1);
		}
		
	//Test MASK File
	sprintf(file_name, "%s", input_addr_file);
	if ((in_addr_file = fopen(file_name, "rb")) == NULL)
		{
			fprintf(stderr,"Could not open addr file : %s\n",file_name);
			exit(1);
		}

	//Test OUTPUT File
	sprintf(file_name, "%s", output_classif);
	if ((class_file = fopen(file_name, "wb")) == NULL)
		{
			fprintf(stderr,"Could not open output file : %s\n",file_name);
			exit(1);
		}
		

	

		
		sprintf(output_dist, "%s_dist", output_classif);
	if ((output_dist_file = fopen(output_dist, "wb")) == NULL)
		{
			fprintf(stderr,"Could not open output file : %s\n",file_name);
			exit(1);
		}
	/*	float zero=0;
	i=0;
	while(i < Ncol * Nlig){
		fwrite(&zero, sizeof(float), 1, class_file);
		i++;
	}
	fclose(class_file);
	class_file = fopen(file_name, "w+");*/

	int num_band_file[Npolar];

//	for(i=9;i<argc;i++){
//		num_band_file[i-9] = atoi(argv[i]);
//	}

	//Test RANGE File
	sprintf(file_name, "%s", range_file);
	range_restore = fopen(file_name, "r");
	restore_scale_param(range_restore,Npolar);
	x = (struct svm_node *) malloc(max_nr_attr*sizeof(struct svm_node));
	if(predict_probability)
	{
		sprintf(file_name, "%s_prob", output_classif);
		if ((prob_file = fopen(file_name, "wb")) == NULL)
		{
			fprintf(stderr,"Could not open prob file : %s\n",file_name);
			exit(1);
		}	
		
		if(svm_check_probability_model(model)==0)
		{
			fprintf(stderr,"Model does not support probabiliy estimates\n");
			exit(1);
		}
	}
	else
	{
		if(svm_check_probability_model(model)!=0)
			printf("Model supports probability estimates, but disabled in prediction.\n");
	}
	printf("\n\nON Y EST!!!\n\n");
	predict(in_file,class_file, output_dist_file,prob_file, predict_probability, in_addr_file,Ncol, Nlig, Npolar);
	svm_destroy_model(model);
	free(x);
	free(line);
	fclose(in_file);
	fclose(in_addr_file);
	fclose(class_file);
	/*fclose(output_dist_file);*/
	/*fclose(prob_file);*/
	return 0;
}
