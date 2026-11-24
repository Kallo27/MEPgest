#ifndef SCHOOL_H
#define SCHOOL_H

#include <QString>

class School
{
    friend class GAmanager;

public:
    School(const QString &name);

    QString getName() const;
    void setName(const QString &name);

    int getId() const;
    int getScore() const;

private:
    QString m_name;
    int m_id;
    int m_score;

    void setId(int id);
    void setScore(int score);
};

#endif // SCHOOL_H
