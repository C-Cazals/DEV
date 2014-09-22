/*
 *      write_best_cv_results.c
 *      
 *      Copyright 2009 cedric <cedric@cedric-laptop>
 *      
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *      
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *      
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 */


/* ROUTINES */
#include "../lib/graphics.h"
#include "../lib/matrix.h"
#include "../lib/processing.h"
#include "../lib/util.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>


/* GLOBAL VARIABLES */
char *config_file, *in_dir,  *out_dir;
char *Npol,  *area_file,   *cluster_file,  *range_file;
char *cluster_file_norm,  *svm_model_file,  *classification_file;
char *Npt_max_classe,  *unbalanced_training,  *new_model,  *cv;
char *log2c_begin,  *log2c_end, *log2c_step,  *log2g_begin;
char *log2g_end, *log2g_step, *kernel_type,  *cost;
char *degree;//,  *gamma;
int Max_Char = 1024;


void write_svm_conf_file(char *config_file, char *in_dir, char *out_dir,
char *Npol, char **input_ind_pol, char *area_file,  char *cluster_file,
char *range_file, char *cluster_file_norm, char *svm_model_file,
char *classification_file,  char *Npt_max_classe,
char *unbalanced_training, char *new_model, char *cv, char *log2c_begin,
char *log2c_end,char *log2c_step, char *log2g_begin,char *log2g_end,
char *log2g_step, char *kernel_type, char *cost, char *degree, char *gamma);

char **read_svm_conf_file(char *config_file, char *in_dir, char *out_dir,
char *Npol, char *area_file,  char *cluster_file, char *range_file,
char *cluster_file_norm, char *svm_model_file, char *classification_file, 
char *Npt_max_classe, char *unbalanced_training, char *new_model, char *cv,
char *log2c_begin, char *log2c_end,char *log2c_step, char *log2g_begin,
char *log2g_end,char *log2g_step,char *kernel_type, char *cost, 
char *degree, char *gamma);

void write_svm_script(char *script_svm, int svm_scale_opt, int svm_cv_grid_opt,
int svm_train_opt, int svm_predict_opt, char *in_dir, char *out_dir,
char *range_file, char *cluster_file, char *cluster_file_norm,
char *file_svm_grid, char *log2c_begin, char *log2c_end, char *log2c_step,
char *log2g_begin, char *log2g_end, char *log2g_step, char *kernel_type,
char *cost, char *degree, char *gamma, char *svm_model_file,
char *unbalanced_training, int *Npt_classe_out, char *classification_file,
char *Npol, char **input_ind_pol);

float *read_cv_file(char *cv_file, float *line_tab_cv);

int main(int argc, char** argv)
{
	char file_name[Max_Char];
	char disable_word[Max_Char];
	sprintf(disable_word, "DISABLE");
	
	char config_file[Max_Char],in_dir[Max_Char], out_dir[Max_Char],Npol[Max_Char], area_file[Max_Char];
	char cluster_file[Max_Char], range_file[Max_Char], cluster_file_norm[Max_Char], svm_model_file[Max_Char];
	char classification_file[Max_Char],  Npt_max_classe[Max_Char], unbalanced_training[Max_Char];
	char new_model[Max_Char], cv[Max_Char], kernel_type[Max_Char], cost[Max_Char], degree[Max_Char], gamma[Max_Char];

	char **input_ind_pol = NULL;
	
	char log2c_begin[Max_Char],log2c_end[Max_Char],log2c_step[Max_Char];
	char log2g_begin[Max_Char],log2g_end[Max_Char],log2g_step[Max_Char];
	
	float *best_tab_cv;	
	
	if (argc == 3) {
		strcpy(in_dir, argv[1]);
		strcpy(config_file, argv[2]);	
	} else{
			edit_error("write_best_cv_results in_dir svm_config_file\n", "");
	} 
		
	input_ind_pol = read_svm_conf_file(config_file, in_dir, out_dir,
		Npol, area_file,  cluster_file, range_file, cluster_file_norm,
		svm_model_file, classification_file, Npt_max_classe,
		unbalanced_training, new_model, cv,log2c_begin, log2c_end,
		log2c_step, log2g_begin,log2g_end,log2g_step,kernel_type, cost, 
		degree, gamma);	
	
	best_tab_cv = calloc(3,sizeof(float));
	sprintf(file_name, "%scross_val.txt", out_dir);
	best_tab_cv = read_cv_file(file_name,best_tab_cv);//We read the best C and Gamma value
				
	//We define the element of the new svm configuration file to a simple RBF classification (Post CV)
	sprintf(cv, "0");//
	sprintf(cost, "%f",best_tab_cv[0]);
	sprintf(gamma, "%f",best_tab_cv[1]);
	sprintf(log2c_begin, "%s", disable_word);
	sprintf(log2c_end, "%s", disable_word);
	sprintf(log2c_step, "%s", disable_word);
	sprintf(log2g_begin, "%s", disable_word);
	sprintf(log2g_end, "%s", disable_word);
	sprintf(log2g_step, "%s", disable_word);
	sprintf(degree, "%s", disable_word);
	
	// We wrtite the new config file with the addition time prefix to the usefull file
	write_svm_conf_file(config_file, in_dir, out_dir, Npol,
		input_ind_pol, area_file,  cluster_file, range_file,
		cluster_file_norm, svm_model_file, classification_file,
		Npt_max_classe, unbalanced_training, new_model, cv, log2c_begin,
		log2c_end, log2c_step,  log2g_begin, log2g_end, log2g_step,
		kernel_type, cost, degree, gamma);
				
	free(best_tab_cv);

	
	return 0;
}

/***************************
**********FONCTIONS*********
 ***************************/


/*******************************************************************************
Routine  : read_cv_file
Authors  : 
Creation : 
Update   : 
-------------------------------------------------------------------------------
Description :  copy a file into an other new file


Inputs  : 


Outputs : 

-------------------------------------------------------------------------------
Inputs arguments :
argc : nb of input arguments
argv : input arguments array
Returned values  :
1
*******************************************************************************/
float *read_cv_file(char *cv_file, float *line_tab_cv)
{
    FILE* file_cv;
	float *line_tab_cv_tmp;
	char buff_1[Max_Char];
	char buff_2[Max_Char];
	char buff_3[Max_Char];
	
	line_tab_cv_tmp = calloc(3,sizeof(float));

	if ((file_cv = fopen(cv_file, "r")) == NULL) {
		fprintf(stderr,"Could not open svm  file : %s\n", cv_file);
		exit(1);
	}

	while(fscanf(file_cv,"%s %s %s",buff_1,buff_2,buff_3)!=EOF){
		if(atof(buff_3) > line_tab_cv[2]){
			line_tab_cv[0] = atof(buff_1);
			line_tab_cv[1] = atof(buff_2);
			line_tab_cv[2] = atof(buff_3);
		}
	}

	fclose(file_cv);
	line_tab_cv[0] = pow(2,line_tab_cv[0]);
	line_tab_cv[1] = pow(2,line_tab_cv[1]);
	
	printf("\nBest (Cost,Gamma)--> Mean accuracy\n(%f,%f) --> %.3f %% \n\n",line_tab_cv[0] ,line_tab_cv[1],line_tab_cv[2]);
    free(line_tab_cv_tmp);
    return line_tab_cv;
}


/*******************************************************************************
Routine  : write_svm_conf_file
Authors  : 
Creation : 
Update   : 
-------------------------------------------------------------------------------
Description :  Write a text file which contain all the classification parameters
Used only in the Case of the Polsarpro Interface

Inputs  : 


Outputs : 

-------------------------------------------------------------------------------
Inputs arguments :
argc : nb of input arguments
argv : input arguments array
Returned values  :
1
*******************************************************************************/
/******** Test à inclure********
 * *****************************
	Si utilisation d'un ANCIEN MODEL
	Si CV
	Si 
 */
void write_svm_conf_file(char *config_file, char *in_dir, char *out_dir, 
char *Npol, char **input_ind_pol, char *area_file,  char *cluster_file, 
char *range_file, char *cluster_file_norm, char *svm_model_file, 
char *classification_file,  char *Npt_max_classe, 
char *unbalanced_training, char *new_model, char *cv, char *log2c_begin,
char *log2c_end,char *log2c_step, char *log2g_begin,char *log2g_end,
char *log2g_step,char *kernel_type, char *cost, char *degree, char *gamma)
{
	int Npolar,i;
	FILE *conf_file;
	
	Npolar = atoi(Npol);

	if ((conf_file = fopen(config_file, "w")) == NULL) {
		fprintf(stderr,"Could not open svm configuration file : %s\n", config_file);
		exit(1);
	}
	
	fprintf(conf_file, "#########################################\n");
	fprintf(conf_file, "# SVM Classification Configuration File #\n");
	fprintf(conf_file, "#########################################\n");
	fprintf(conf_file, "# 'DISABLE' is the argument for All\n");
	fprintf(conf_file, "# UNUSED parameters\n");
	fprintf(conf_file, "\n");
	
	fprintf(conf_file, "#####################\n");
	fprintf(conf_file, "# Working directory #\n");
	fprintf(conf_file, "#####################\n");
	fprintf(conf_file, "in_dir %s\n",in_dir); //Directory which content the input polarimetric indicators
	fprintf(conf_file, "out_dir %s\n",out_dir); //Output Directory
	fprintf(conf_file, "\n");
	
	fprintf(conf_file, "###############\n");
	fprintf(conf_file, "# Input files #\n");
	fprintf(conf_file, "###############\n");
	fprintf(conf_file, "number_of_pol_indic %s\n",Npol); //Number of the input polarimetric indicators
	fprintf(conf_file, "name_of_pol_indic ");	//Name of the input polarimetric indicators
	for(i=0;i<Npolar;i++){
		fprintf(conf_file, "%s ",input_ind_pol[i]);
	}
	fprintf(conf_file, "\n");
	fprintf(conf_file, "\n");
	
	fprintf(conf_file, "########################\n");
	fprintf(conf_file, "# Name of working file #\n");
	fprintf(conf_file, "########################\n");
	fprintf(conf_file, "area_file %s\n", area_file); //Name of the text file which contain the Region of interest
	fprintf(conf_file, "training_file %s\n",cluster_file); //Name of the output training file
	fprintf(conf_file, "range_file %s\n", range_file); //Name of the file which contain the normalize parameters for each polarimetric indicator
	fprintf(conf_file, "training_file_norm %s\n",cluster_file_norm); //Name of the NORMALIZED output training file
	fprintf(conf_file, "svm_model_file %s\n",svm_model_file); //Name of the output SVM model file
	fprintf(conf_file, "output_file_classif %s\n", classification_file); //Name of the output classification
	fprintf(conf_file, "\n");
	
	fprintf(conf_file, "##################\n");
	fprintf(conf_file, "# SVM Parameters #\n");
	fprintf(conf_file, "##################\n");
	fprintf(conf_file, "max_number_of_training_points %s\n",Npt_max_classe ); // Max Number of training point among those in the area_file, 0 IF all the area_file points 
	fprintf(conf_file, "unbalanced_training_dataset %s\n", unbalanced_training); // Option to balance the Cost parameter of each classes in function of the class withe the max number of training point. 1 to ENABLE, 0 to DISABLE
	fprintf(conf_file, "new_model %s\n", new_model);// Option which alow to use an older SVM model file. 0 to create a New model, 1 to use an older model
	fprintf(conf_file, "CV %s\n",cv);	
	fprintf(conf_file, "CV_log2c_interval %s %s %s\n",log2c_begin,log2c_end, log2c_step);
	fprintf(conf_file, "CV_log2g_interval %s %s %s\n",log2g_begin,log2g_end, log2g_step);
	fprintf(conf_file, "kernel_type %s\n", kernel_type);	
	fprintf(conf_file, "cost %s\n", cost);
	fprintf(conf_file, "degree %s\n", degree);
	fprintf(conf_file, "gamma %s\n",gamma);	
	
	fclose(conf_file);

}


/*******************************************************************************
Routine  : read_svm_conf_file
Authors  : 
Creation : 
Update   : 
-------------------------------------------------------------------------------
Description :  Read the svm configuration file and return their parameters


Inputs  : 


Outputs : 

-------------------------------------------------------------------------------
Inputs arguments :
argc : nb of input arguments
argv : input arguments array
Returned values  :
1
*******************************************************************************/
char **read_svm_conf_file(char *config_file, char *in_dir, char *out_dir,
char *Npol, char *area_file,  char *cluster_file, char *range_file,
char *cluster_file_norm, char *svm_model_file, char *classification_file, 
char *Npt_max_classe, char *unbalanced_training, char *new_model, char *cv,
char *log2c_begin, char *log2c_end,char *log2c_step, char *log2g_begin,
char *log2g_end,char *log2g_step,char *kernel_type, char *cost, 
char *degree, char *gamma)
{
	FILE *conf_file;
	char buff_ligne[Max_Char];
	char **input_ind_pol=NULL;
	int i,Npolar;
	
	conf_file = fopen(config_file, "r");	
	
	for(i=0;i<9;i++){// Loop to skip the header of the svm configuration file and the Working directory header
		fgets(buff_ligne, Max_Char, conf_file);
	}
	fscanf(conf_file,"%s %s",buff_ligne,in_dir);
	fscanf(conf_file,"%s %s",buff_ligne,out_dir);
	
	for(i=0;i<5;i++){// Loop to skip the Input file header
	fgets(buff_ligne, Max_Char, conf_file);
	}
	fscanf(conf_file,"%s %s",buff_ligne,Npol);

	Npolar = atoi(Npol);
	
	input_ind_pol = malloc(Npolar*sizeof(char*));// Allocation of the input polarimetric indicators name table
	for(i=0;i<Npolar;i++){
		input_ind_pol[i] = malloc(Max_Char * sizeof(char));
	}
	fscanf(conf_file,"%s",buff_ligne); //To skip the 'name_of_pol_indic' flag
	for(i=0;i<Npolar;i++){ //Loop to write the name of the polarimetric indicators in the input_ind_pol tab
		fscanf(conf_file,"%s",input_ind_pol[i]);
	}
	
	for(i=0;i<5;i++){// Loop to skip the 'Name of working file' header
	fgets(buff_ligne, Max_Char, conf_file);
	}
	
	fscanf(conf_file,"%s %s",buff_ligne,area_file);
	fscanf(conf_file,"%s %s",buff_ligne,cluster_file);
	fscanf(conf_file,"%s %s",buff_ligne,range_file);
	fscanf(conf_file,"%s %s",buff_ligne,cluster_file_norm);
	fscanf(conf_file,"%s %s",buff_ligne,svm_model_file);
	fscanf(conf_file,"%s %s",buff_ligne,classification_file);	

	for(i=0;i<5;i++){// Loop to skip the 'SVM Parameters' header
	fgets(buff_ligne, Max_Char, conf_file);
	}

	fscanf(conf_file,"%s %s",buff_ligne,Npt_max_classe);
	fscanf(conf_file,"%s %s",buff_ligne,unbalanced_training);
	fscanf(conf_file,"%s %s",buff_ligne,new_model);
	fscanf(conf_file,"%s %s",buff_ligne,cv);	
	fscanf(conf_file,"%s %s %s %s",buff_ligne,log2c_begin, log2c_end, log2c_step);
	fscanf(conf_file,"%s %s %s %s",buff_ligne,log2g_begin, log2g_end, log2g_step);
	fscanf(conf_file,"%s %s",buff_ligne,kernel_type);
	fscanf(conf_file,"%s %s",buff_ligne,cost);	
	fscanf(conf_file,"%s %s",buff_ligne,degree);
	fscanf(conf_file,"%s %s",buff_ligne,gamma);	

	fclose(conf_file);
	
	return input_ind_pol;
}
