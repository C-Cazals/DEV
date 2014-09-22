#include <float.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
/* This routine is modify to be apply to bynary data contrary to (initialy) .txt file */

/* LOCAL PROCEDURES */
int cmp(const void* elem1, const void* elem2)
{
    if(*(const float*)elem1 < *(const float*)elem2)
        return -1;
    return *(const float*)elem1 > *(const float*)elem2;
}
/*
static int cmp (const void *a, const void *b)
{
   int ret = 0;
   float const *pa = a;
   float const *pb = b;
   float diff = *pa - *pb;
   if (diff > 0)
   {
      ret = 1;
   }
   else if (diff < 0)
   {
      ret = -1;
   }

   return ret;
}*/

void exit_with_help()
{
	printf(
	"Usage: svm-scale percentage range_file input_bin output_bin number_of_polarimetric_indices\n"//CHANGE
	);
	exit(1);
}

char *line = NULL;
int max_line_len = 1024;
double lower=-1.0,upper=1.0,y_lower,y_upper;
int y_scaling = 0;
double *feature_max;
double *feature_min;
double y_max = -DBL_MAX;
double y_min = DBL_MAX;
int max_index;
long int num_nonzeros = 0;
long int new_num_nonzeros = 0;
int Npolar;/* Number of polarimetric indices used in the classification*/

#define max(x,y) (((x)>(y))?(x):(y))
#define min(x,y) (((x)<(y))?(x):(y))

float output_target(double value);
float output(int index, double value);
char* readline(FILE *input);

/* Fonction Polsarpro*/
void check_dir(char *dir);
void read_config(char *dir, int *Nlig, int *Ncol, char *PolarCase, char *PolarType);
float **matrix_float(int nrh,int nch);
void free_matrix_float(float **m,int nrh);
void edit_error(char *s1,char *s2);
void check_file(char *file);
void check_dir(char *dir);
float *vector_float(int nrh);
void free_vector_float(float *m);
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
Routine  : check_dir
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Checks and corrects slashes in directory string
*-------------------------------------------------------------------------------
Inputs arguments :
dir    : string to be checked
Returned values  :
void
*******************************************************************************/
void check_dir(char *dir)
{
#ifndef _WIN32
    strcat(dir, "/");
#else
    int i;
    i = 0;
    while (dir[i] != '\0') {
	if (dir[i] == '/')
	    dir[i] = '\\';
	i++;
    }
    strcat(dir, "\\");
#endif
}

/*******************************************************************************
Routine  : read_config
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Read a configuration file
*-------------------------------------------------------------------------------
Inputs arguments :
dir    : location of the config.txt file
Returned values  :
Nlig   : Read number of lines
Ncol   : Read number of rows
PolarCase : Monostatic / Bistatic
PolarType : Full / PP1 / PP2 / PP3 / PP4
*******************************************************************************/
void
read_config(char *dir, int *Nlig, int *Ncol, char *PolarCase,
	    char *PolarType)
{
    char file_name[1024];
    char Tmp[1024];
    FILE *file;

    sprintf(file_name, "%sconfig.txt", dir);
    if ((file = fopen(file_name, "r")) == NULL)
	edit_error("Could not open configuration file : ", file_name);


    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%i\n", &*Nlig);
    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%i\n", &*Ncol);
    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%s\n", PolarCase);
    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%s\n", Tmp);
    fscanf(file, "%s\n", PolarType);

    fclose(file);
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
Returned values  :
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

/*******************************************************************************
Routine  : check_file
Authors  : Eric POTTIER, Laurent FERRO-FAMIL
Creation : 01/2002
Update   :
*-------------------------------------------------------------------------------
Description :  Checks and corrects slashes in file string
*-------------------------------------------------------------------------------
Inputs arguments :
file    : string to be checked
Returned values  :
void
*******************************************************************************/
void check_file(char *file)
{
#ifdef _WIN32
    int i;
    i = 0;
    while (file[i] != '\0') {
	if (file[i] == '/')
	    file[i] = '\\';
	i++;
    }
#endif
}


int main(int argc,char **argv)
{
	int i;
	FILE *out_put,*in_put, *fp_restore = NULL;
	char range_file[1024];
	char input_bin[1024], output_bin[1024];
	char restore_filename[1024];
	
	int ind_min, ind_max, num_pix, npol, pix;
	float prct=0;
	float **Tmp_in, *Tmp;
	

    if (argc == 6) {
		prct = atof(argv[1]);
		strcpy(range_file, argv[2]);
		strcpy(input_bin, argv[3]);
		strcpy(output_bin, argv[4]);
		Npolar = atoi(argv[5]);
    } else
	edit_error
	    ("svm-scale_polsarpro percentage range_file input_bin output_bin number_of_polarimetric_indices\n", "");

	strcpy(restore_filename,"0");
	printf("prct : %f\n", prct);
	printf("restore_filename : %s\n", restore_filename);
	printf("range_file : %s\n", range_file);
printf("input_bin : %s\n", input_bin);
printf("output_bin : %s\n", output_bin);



	in_put=fopen(input_bin,"rb");
	if(in_put==NULL)
	{
		fprintf(stderr,"can't open input file %s\n", input_bin);
		exit(1);
	}

	out_put = fopen(output_bin,"wb");	
	if(out_put == NULL)
	{
		fprintf(stderr,"can't open output file %s\n",output_bin);
		exit(1);
	}

	if(Npolar<1)
	{
		fprintf(stderr,"the number of polarimetric indices is missing or to low\n");
		exit(1);
	}
	float pixel[Npolar + 1];

	if(!(upper > lower) || (y_scaling && !(y_upper > y_lower)))
	{
		fprintf(stderr,"inconsistent lower/upper specification\n");
		exit(1);
	}
	
	/*if(restore_filename && range_file)
	{
		fprintf(stderr,"cannot use -r and -s simultaneously\n");
		exit(1);
	}
*/
#define SKIP_TARGET\
	while(isspace(*p)) ++p;\
	while(!isspace(*p)) ++p;

#define SKIP_ELEMENT\
	while(*p!=':') ++p;\
	++p;\
	while(isspace(*p)) ++p;\
	while(*p && !isspace(*p)) ++p;
	

	/* pass 1: find out min/max value */
	feature_max = (double *)malloc((Npolar)* sizeof(double));
	feature_min = (double *)malloc((Npolar)* sizeof(double));

	if(feature_max == NULL || feature_min == NULL)
	{
		fprintf(stderr,"can't allocate enough memory\n");
		exit(1);
	}

	for(i=0;i<Npolar;i++)
	{
		feature_max[i]=-DBL_MAX;
		feature_min[i]=DBL_MAX;
	}	

	num_pix = 0;
	
	while(fread(&pixel, sizeof(float), Npolar +1, in_put)!=0){
		num_pix++;
	}
	rewind(in_put);
	
	printf("num_pix : %i\n", num_pix);
	
	ind_min = (int)floor(prct*(float)num_pix/100.);
	ind_max = (int)floor((100 - prct)*(float)num_pix/100)-1;
	
	printf("ind_min : %i\n", ind_min);
	printf("ind_max : %i\n", ind_max);

	Tmp_in = matrix_float(Npolar,num_pix);	
	Tmp = vector_float(num_pix);
	for (pix = 0; pix < num_pix; pix++) {
		fread(&pixel, sizeof(float), Npolar +1, in_put);
		float *p=pixel;
		y_max = max(y_max,p[0]);
		y_min = min(y_min,p[0]);
		
		for (npol = 0; npol < Npolar; npol++){
			Tmp_in[npol][pix] = pixel[npol + 1];
		}
	}
	rewind(in_put);

	for (npol = 0; npol < Npolar; npol++){
		for (pix = 0; pix < num_pix; pix++) {
			Tmp[pix] = Tmp_in[npol][pix];
		}
		qsort(Tmp, num_pix, sizeof *Tmp, cmp);

		feature_min[npol] = Tmp[ind_min];
		feature_max[npol] = Tmp[ind_max];
	}
	
	/* pass 1.5: save/restore feature_min/feature_max */
	
	if(strcmp(restore_filename,"1")==1)
	{
		/* fp_restore rewinded in finding max_index */
		int idx, c;
		double fmin, fmax;
		
		if((c = fgetc(fp_restore)) == 'y')
		{
			fscanf(fp_restore, "%lf %lf\n", &y_lower, &y_upper);
			fscanf(fp_restore, "%lf %lf\n", &y_min, &y_max);
			y_scaling = 1;
		}
		else
			ungetc(c, fp_restore);

		if (fgetc(fp_restore) == 'x') {
			fscanf(fp_restore, "%lf %lf\n", &lower, &upper);
			while(fscanf(fp_restore,"%d %lf %lf\n",&idx,&fmin,&fmax)==3)
			{
				if(idx<=max_index)
				{
					feature_min[idx] = fmin;
					feature_max[idx] = fmax;
				}
			}
		}
		fclose(fp_restore);
	}

//	if(strcmp(restore_filename,"1")==1)
//	{
		FILE *fp_save = fopen(range_file,"w");
		if(fp_save==NULL)
		{
			fprintf(stderr,"can't open file %s\n", range_file);
			exit(1);
		}
		if(y_scaling)
		{
			fprintf(fp_save, "y\n");
			fprintf(fp_save, "%.16g %.16g\n", y_lower, y_upper);
			fprintf(fp_save, "%.16g %.16g\n", y_min, y_max);
		}
		fprintf(fp_save, "x\n");
		fprintf(fp_save, "%.16g %.16g\n", lower, upper);
		for(i=0;i<Npolar;i++)
		{
			if(feature_min[i]!=feature_max[i])
				fprintf(fp_save,"%d %.16g %.16g\n",i+1,feature_min[i],feature_max[i]);
		}
		fclose(fp_save);
//	}

	/* pass 2: scale */

	while(fread(&pixel, sizeof(float), Npolar +1, in_put)!=0)
	{
		float *p=pixel;
		float target;

		target = p[0];
		target = output_target(target);
		fwrite(&target, sizeof(float), 1, out_put);

		for (i= 1;i < Npolar + 1; i++)
		{
		p[i] = output(i-1,p[i]);
		fwrite(&p[i], sizeof(float), 1, out_put);
		}
	}
	free_vector_float(Tmp);
	free_matrix_float(Tmp_in,Npolar);
	free(feature_max);
	free(feature_min);
	fclose(in_put);
	fclose(out_put);
	return 0;
}

char* readline(FILE *input)
{
	int len;
	
	if(fgets(line,max_line_len,input) == NULL)
		return NULL;

	while(strrchr(line,'\n') == NULL)
	{
		max_line_len *= 2;
		line = (char *) realloc(line, max_line_len);
		len = (int) strlen(line);
		if(fgets(line+len,max_line_len-len,input) == NULL)
			break;
	}
	return line;
}


float output_target(double value)
{
	if(y_scaling)
	{
		if(value == y_min)
			value = y_lower;
		else if(value == y_max)
			value = y_upper;
		else value = y_lower + (y_upper-y_lower) *
			     (value - y_min)/(y_max-y_min);
	}
	return (float)value;
}

float output(int index, double value)
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
return (float)value;
}
