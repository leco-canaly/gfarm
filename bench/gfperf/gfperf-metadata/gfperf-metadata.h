/*
 * $Id$
 */


/* $id */
#include <sys/time.h>

#ifndef _GFPERF_METADATA_H_
#define _GFPERF_METADATA_H_

#define MKDIR_MODE 0755
#define CHMOD_MODE 0700
#define XATTR_KEY "gfarm.ncopy"
#define BUF_SIZE 1024

#define UNIT_OPS "ops"
#define UNIT_USEC "usec"
#define UNIT_FLAG_UNDEF 0
#define UNIT_FLAG_OPS 1
#define UNIT_FLAG_USEC 2

struct directory_names {
	int n;
	char *names[0];
};

struct test_results {
	int number;
	struct timeval start;
	struct timeval middle;
	struct timeval end;
	float startup;
	float average;
};

extern int libgfarm_flag;
extern char *testdir;
extern char *rootdir;
extern int loop_number;
extern char *unit;
extern int unit_flag;

gfarm_error_t do_posix_test(struct directory_names *names);
gfarm_error_t do_libgfarm_test(struct directory_names *names);

struct directory_names *create_directory_names(int n, char *postfix);
void free_directory_names(struct directory_names *p);

void set_number(struct test_results *r, int n);
void set_start(struct test_results *r);
void set_middle(struct test_results *r);
void set_end(struct test_results *r);
void calc_result(struct test_results *r);
void adjust_result(struct test_results *r);
#endif
