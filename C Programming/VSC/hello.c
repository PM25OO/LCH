#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
  int number;
  struct node *next;
} node;

int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    printf("Usage: %s number1 number2 ...\n", argv[0]);
    return 1;
  }

  node *list = NULL;

  // Insert the first number
  int number = atoi(argv[1]);
  node *n = malloc(sizeof(node));
  if (n == NULL)
  {
    return 1;
  }
  n->number = number;
  n->next = list;
  list = n;

  // Insert the remaining numbers
  for (int i = 2; i < argc; i++)
  {
    number = atoi(argv[i]);
    n = malloc(sizeof(node));
    if (n == NULL)
    {
      return 1;
    }
    n->number = number;
    n->next = NULL;

    if (number <= list->number)
    {
      n->next = list;
      list = n;
    }
    else
    {
      node *current = list;
      while (current->next != NULL && current->next->number < number)
      {
        current = current->next;
      }
      n->next = current->next;
      current->next = n;
    }
  }

  // Print the list
  node *ptr = list;
  while (ptr != NULL)
  {
    printf("%d ", ptr->number);
    ptr = ptr->next;
  }
  printf("\n");

  // Free the allocated memory
  ptr = list;
  while (ptr != NULL)
  {
    node *temp = ptr;
    ptr = ptr->next;
    free(temp);
  }

  return 0;
}