#ifndef SCHOOL_H
#define SCHOOL_H

#include <QString>

class School
{
private:
    QString m_name;
    int m_id;
    int m_score;

public:
    School(const QString &name);

    QString getName() const;
    void setName(const QString &name);

    int getId() const;
    void setId(int id);

    int getScore() const;
    void setScore(int score);
};

#endif // SCHOOL_H
