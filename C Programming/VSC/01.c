char *match(char *s, char ch)
{
    char *last = NULL;
    do
    {
        if (*s == ch)
        {
            last = s;
        }
        s++;
    } while (*s);
    return last;
}